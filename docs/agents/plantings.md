# Plantings

## Overview

Full-stack CRUD for plantings at `api/{API_VERSION}/plantings/` (backend) and `/plantings` (frontend, route `plantings`). A planting links a `Crop` and `Variety` and carries daily observations. `PlantingGrowthStage` is a model-only entity (no API).

## Backend (`backend/greenhouse/`)

### Models

`models/planting.py` -> `Planting`

- `user` FK (`related_name="plantings"`, CASCADE), `crop` FK, `variety` FK.
- `status` (default ACTIVE; choices ACTIVE / HARVESTED / DEAD / REMOVED).
- `created_at` (auto_now_add), `updated_at` (auto_now). Meta `ordering = ["-created_at"]` (list view overrides ordering).
- Reverse relations: `locations` (assignments), `daily_observations`, `stages`.

`models/planting_growth_stage.py` -> `PlantingGrowthStage` (no serializer/view/url/OpenAPI)

- `planting` FK (`related_name="stages"`, CASCADE), `stage` (SOWING/GERMINATION/TRANSPLANTING/VEGETATIVE/FLOWERING/FRUITING/HARVEST), `image`, `notes`. No Meta.

`models/planting_daily_observation.py` -> `PlantingDailyObservation`

- `planting` FK (`related_name="daily_observations"`, CASCADE), `stage` FK (nullable, SET_NULL).
- Choice sets: health (GOOD/FAIR/POOR), pest (NONE/LOW/MEDIUM/HIGH), fertilizer (NONE/ORGANIC/SYNTHETIC), watering (WATERED/RAINED/SKIPPED_WET).
- Health/pest/disease/pruning/fertilizer/flowering/fruiting fields, `notes`, `image` (`upload_to="observations/"`), `observation_date` (default today), timestamps.

### Serializers

- `serializers/planting.py` -> `PlantingSerializer`: writable `crop`/`variety` (PK fields scoped per-user in `get_fields`), `status`; computed `crop_name`, `variety_name`, `current_location` (open-ended assignment), `has_daily_observation`, `age_in_days`, `created_at`. `validate` ensures variety belongs to crop.
- `serializers/planting_daily_observation.py` -> `PlantingDailyObservationSerializer` (`stage` read-only + `stage_name`; multipart image; `update` clears old image when removed) and `PlantingDailyObservationBulkCreateSerializer` (`planting_ids` validated per-user; creates one observation per planting in a transaction).

### Views

`views/planting.py`:

- `PlantingListApiView` (list + create): `SearchFilter` on `crop__name`/`variety__name`; annotates `has_daily_observation` (Exists for today); orders ACTIVE first then `-created_at`.
- `PlantingDetailApiView` (retrieve/update/destroy).

`views/planting_daily_observation.py`:

- `PlantingDailyObservationListApiView` (list + create, `MultiPartParser`).
- `PlantingDailyObservationDetailApiView` (update/destroy only, no retrieve).
- `PlantingDailyObservationBulkCreateApiView` (POST, `JSONParser`, 201).

### URLs

`urls/planting.py`:

- `"observations/bulk/"` -> bulk create (`planting-daily-observation-bulk-create`).
- `""` -> `PlantingListApiView` (`planting-list-create`).
- `"<int:pk>"` -> `PlantingDetailApiView` (`planting-detail`).
- `"<int:planting_pk>/locations/"` -> include `planting_location_assignment`.
- `"<int:planting_pk>/observations/"` -> include `planting_daily_observation`.

`urls/planting_daily_observation.py`: `""` (list-create), `"<int:pk>"` (detail).

### OpenAPI

`openapi/planting/` and `openapi/planting_daily_observation/`. No `planting_growth_stage` directory.

### Tests

- `tests/planting.py`: `PlantingListApiViewTests`, `PlantingCreateApiViewTests`, `PlantingGetApiViewTests`, `PlantingUpdateApiViewTests`, `PlantingPartialUpdateApiViewTests`, `PlantingDeleteApiViewTests`, `PlantingCurrentLocationTests`, `PlantingHasDailyObservationTests`, `PlantingAgeInDaysTests`.
- `tests/planting_daily_observation.py`: `PlantingDailyObservationListApiViewTests`, `PlantingDailyObservationCreateApiViewTests`, `PlantingDailyObservationDetailApiViewTests`, `PlantingDailyObservationImageClearTests`, `PlantingDailyObservationBulkCreateApiViewTests`.

Discovery gotcha: `tests/__init__.py` only re-exports a subset. Not re-exported (will silently not run): `PlantingCurrentLocationTests`, `PlantingHasDailyObservationTests`, `PlantingAgeInDaysTests`, `PlantingDailyObservationImageClearTests`, `PlantingDailyObservationBulkCreateApiViewTests`.

Factories: `PlantingFactory`, `PlantingDailyObservationFactory`.

## Frontend (`frontend/src/`)

### View

`views/plantings/index.vue` (`PlantingsView`). Orchestrates search (debounced 500ms), pagination, create/update/delete, locations sheet, daily-observation sheet, and bulk observation dialog. Uses `usePlantings` and `useBulkCreateObservation`.

### Components

`components/plantings/`:

- `PlantingColumns.ts`, `PlantingCreateDialog.vue`, `PlantingUpdateDialog.vue`, `PlantingsTable.vue` (row selection + bulk toolbar), `PlantingTableActions.vue`.

`components/plantings/daily-observation/`:

- `constants.ts`, `PlantingDailyObservationCreateDialog.vue`, `PlantingDailyObservationUpdateDialog.vue`, `PlantingDailyObservationViewDialog.vue`, `PlantingDailyObservationSheet.vue`, `PlantingDailyObservationBulkCreateDialog.vue`.

### Composables

- `composables/usePlantings.ts` -> key `["plantings", pagination, "search"]`; mutations invalidate `["plantings"]`.
- `composables/usePlantingDailyObservations.ts` -> key `["planting-daily-observations", plantingId, pagination]`; create/delete also invalidate `["plantings"]`.
- `composables/useBulkCreateObservation.ts` -> single `bulkCreate` mutation, invalidates `["plantings"]`.

### API services

- `plantingService.ts` (`getAll`/`create`/`update`/`delete` on `/plantings/`).
- `plantingDailyObservationService.ts` (`getAll`/`create`/`update`/`delete` nested under `/plantings/${plantingId}/observations/`; `bulkCreate` -> POST `/plantings/observations/bulk/` with JSON `{ planting_ids, ...payload }`).

### Schemas & types

- `schemas/planting.schemas.ts` (`PLANTING_STATUSES`, `plantingSchema`).
- `schemas/plantingDailyObservation.schemas.ts` (`plantingDailyObservationSchema`).
- `types/planting.ts`, `types/plantingDailyObservation.ts`.

### Tests

`tests/views/plantingsView.spec.ts`, composables (`usePlantings`, `usePlantingDailyObservations`, `useBulkCreateObservation`), services (`plantingService`, `plantingDailyObservationService`), schemas, and component specs under `tests/components/plantings/` (including `daily-observation/`).

## Conventions & gotchas

- `has_daily_observation` and `current_location` are computed/annotated, not persisted fields.
- Plantings list order is ACTIVE first then `-created_at` (overrides model default).
- Observation create/update is multipart (has image); bulk endpoint is JSON-only (no image).
- `api/client.ts` auto-converts snake_case<->camelCase; the bulk endpoint explicitly sends `planting_ids`.
- Several backend test classes are not re-exported in `tests/__init__.py` and will not run (see Tests).
