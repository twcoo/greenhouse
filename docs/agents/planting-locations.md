# Planting Locations

## Overview

Full-stack management of planting locations and their status history. Spans three backend entities: `PlantingLocation`, `PlantingLocationStatus`, and `PlantingLocationAssignment` (assignments are nested under Plantings). Frontend route is `/planting-locations`.

Backend URL prefixes:

- `api/{API_VERSION}/planting-locations/` -> locations and statuses.
- `api/{API_VERSION}/plantings/<planting_pk>/locations/` -> assignments (nested under plantings).

## Backend (`backend/greenhouse/`)

### Models

`models/planting_location.py` -> `PlantingLocation`

- `user` FK -> `User` (`related_name="planting_locations"`, CASCADE).
- `name` (50), `location_type` (`NURSERYPOT` / `POT` / `GROUND`).
- `height`, `length` (Decimal nullable), `width` (Decimal required).
- `created_at` (auto_now_add), `updated_at` (auto_now).
- Meta: `ordering = ["-created_at"]`; indexes `pl_user_created_idx` + trigram `GinIndex` on `name`.

`models/planting_location_status.py` -> `PlantingLocationStatus`

- `planting_location` FK (`related_name="status_history"`, CASCADE).
- `status` (AVAILABLE / IN_USE / DAMAGED / DESTROYED / RETIRED).
- `image` (ImageField `upload_to="locations/"`, nullable), `notes` (TextField).
- `created_at` (auto_now quirk), `updated_at`. No Meta.

`models/planting_location_assignment.py` -> `PlantingLocationAssignment`

- `planting` FK -> `Planting` (`related_name="locations"`, CASCADE).
- `planting_location` FK -> `PlantingLocation` (`on_delete=PROTECT`).
- `start_date`, `end_date` (nullable; null = still assigned).
- `created_at` (auto_now quirk), `updated_at`. No Meta.

### Serializers

- `serializers/planting_location.py` -> `PlantingLocationSerializer`: exposes `id, name, location_type, height, width, length, current_status` (`SerializerMethodField` returns latest status or None). `validate` enforces type rules (GROUND needs `length`, rejects `height`; NURSERYPOT/POT need `height`, reject `length`).
- `serializers/planting_location_status.py` -> `PlantingLocationStatusSerializer`: `id, status, notes, image, created_at`; `validate_image` via `validate_image_file`.
- `serializers/planting_location_assignment.py` -> `PlantingLocationAssignmentSerializer`: `id, planting_location, planting_location_name, start_date, end_date, created_at, updated_at`. `get_fields` scopes `planting_location` to user. `validate` enforces date order, no duplicate open-ended assignment, date overlap, and pot occupancy rules (uses `planting` from serializer context).

### Views

All views use `CustomAuthentication` + `IsAuthenticated` and scope to `request.user`; they are mixin-based `GenericAPIView`s (not DRF ViewSets), decorated with `@extend_schema_view` (tags "Planting Location", "Planting Location Status", "Planting Location Assignment").

- `views/planting_location.py`: `PlantingLocationListApiView` (`SearchFilter` on `name`/`location_type`; `perform_create` seeds an `AVAILABLE` status atomically), `PlantingLocationDetailAPIView` (`perform_destroy` blocks delete while open-ended assignment exists and catches `ProtectedError`).
- `views/planting_location_status.py`: `PlantingLocationStatusListApiView` (`MultiPartParser`; `perform_create` blocks status change while latest status is `IN_USE`).
- `views/planting_location_assignment.py`: `PlantingLocationAssignmentListApiView` (`perform_create` seeds `IN_USE` for pot/nursery-pot), `PlantingLocationAssignmentDetailApiView` (`perform_update` seeds `AVAILABLE` when a pot assignment transitions from open to closed).

### URLs

- `urls/planting_location.py`: `""` (list-create), `"<int:pk>"` (detail), `"<int:pk>/statuses/"` (include `planting_location_status`).
- `urls/planting_location_status.py`: `""` (list-create).
- `urls/planting_location_assignment.py`: `""` (list-create), `"<int:pk>"` (detail); included from `urls/planting.py` at `.../plantings/<planting_pk>/locations/`.

### OpenAPI

`openapi/planting_location/`, `openapi/planting_location_status/`, `openapi/planting_location_assignment/` (each with examples/parameters/responses/schemas).

### Tests

- `tests/planting_location.py`: `PlantingLocationListApiViewTests`, `PlantingLocationCreateApiViewTests`, `PlantingLocationGetApiViewTests`, `PlantingLocationUpdateApiViewTests`, `PlantingLocationPartialUpdateApiViewTests`, `PlantingLocationDeleteApiViewTests`.
- `tests/planting_location_status.py`: `PlantingLocationStatusListApiViewTests`, `PlantingLocationStatusCreateApiViewTests`, `PlantingLocationCurrentStatusTests`.
- `tests/planting_location_assignment.py`: list/create/get/update/partial/delete classes + `PlantingLocationStatusAutoSyncTests`.

All re-exported in `tests/__init__.py`. Factories: `PlantingLocationFactory`, `PlantingLocationStatusFactory`, `PlantingLocationAssignmentFactory`, `PlantingFactory`.

## Frontend (`frontend/src/`)

### View

`views/planting-locations/index.vue` (`PlantingLocationsView`). Manages search (debounced 500ms), pagination, create/update dialogs, and the status sheet. Composes `PlantingLocationTable`, `PlantingLocationCreateDialog`, `PlantingLocationUpdateDialog`, `PlantingLocationStatusSheet`.

### Components

`components/planting-locations/`:

- `PlantingLocationTable.vue`, `PlantingLocationColumns.ts`, `PlantingLocationTableActions.vue`.
- `PlantingLocationCreateDialog.vue`, `PlantingLocationUpdateDialog.vue`.

`components/planting-locations/status/`:

- `PlantingLocationStatusSheet.vue`, `PlantingLocationSetStatusDialog.vue` (manual status limited to DAMAGED/DESTROYED/RETIRED).

`components/planting-location-assignments/`:

- `PlantingLocationAssignmentSheet.vue`, `PlantingLocationAssignmentCreateDialog.vue`, `PlantingLocationAssignmentUpdateDialog.vue`.

### Composables

- `composables/usePlantingLocations.ts` -> `usePlantingLocations(pagination?, searchTerm?)`; key `["planting-locations", pagination, "search"]`.
- `composables/usePlantingLocationStatuses.ts` -> `usePlantingLocationStatuses(locationId, pagination?)`; key `["planting-location-statuses", locationId, pagination]`.
- `composables/usePlantingLocationAssignments.ts` -> `usePlantingLocationAssignments(plantingId, pagination?)`; key `["planting-location-assignments", plantingId, pagination]`; mutations also invalidate `["plantings"]` and `["planting-locations"]`.

### API services

- `plantingLocationService.ts` (GET/POST/PUT/DELETE `/planting-locations/`).
- `plantingLocationStatusService.ts` (GET/POST `/planting-locations/${locationId}/statuses/`, multipart create).
- `plantingLocationAssignmentService.ts` (nested under `/plantings/${plantingId}/locations/`).

### Schemas & types

- `schemas/plantingLocation.schemas.ts` (`LocationTypeEnum`, `plantingLocationSchema` with type-specific height/length refinements).
- `schemas/plantingLocationStatus.schemas.ts` (`MANUAL_STATUS_CHOICES`, `plantingLocationStatusSchema`).
- `schemas/plantingLocationAssignment.schemas.ts` (`plantingLocationAssignmentSchema` with endDate >= startDate).
- `types/plantingLocation.ts`, `types/plantingLocationStatus.ts`, `types/plantingLocationAssignment.ts`.

### Tests

`tests/views/plantingLocationsView.spec.ts`, service/composable/schema specs, and component specs under `tests/components/planting-locations/` and `tests/components/planting-location-assignments/`.

## Conventions & gotchas

- Status auto-sync coupling: create location -> AVAILABLE; assign to pot/nursery -> IN_USE; close pot assignment -> AVAILABLE; ground locations never auto-create statuses.
- `PlantingLocationStatus` and `PlantingLocationAssignment` use `auto_now=True` on `created_at` and have no `Meta`.
- `PlantingLocationAssignment.planting_location` uses `on_delete=PROTECT`.
- Assignment status auto-sync on delete is only tested, not implemented in `perform_destroy` (currently just calls `super()`). Flag this gap if touched.
