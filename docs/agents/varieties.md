# Varieties

## Overview

Full-stack CRUD for crop varieties at `api/{API_VERSION}/varieties/` (backend) and `/varieties` (frontend, route `varieties`). A variety belongs to a `Crop`; ownership is derived from `crop.user`.

## Backend (`backend/greenhouse/`)

### Model

`models/variety.py` -> `Variety`

- `name` (50).
- `crop` FK -> `Crop` (CASCADE); owner scoping via `crop.user`.
- `growth_habit` = Postgres `ArrayField(CharField(choices=GROWTH_HABIT_CHOICES))`, choices DETERMINATE / INDETERMINATE.
- `created_at` (auto_now, NOT auto_now_add), `updated_at` (auto_now).
- Meta: `ordering = ["-created_at"]`; indexes `variety_crop_created_idx` and trigram `GinIndex` on `name`.

### Serializer

`serializers/variety.py` -> `VarietySerializer` (decorated `@extend_schema_serializer`).

- `id` (read-only), `name`, `crop` (`PrimaryKeyRelatedField`, queryset set per-user in `get_fields()`), `crop_name` (`SerializerMethodField`), `growth_habit` (list of choices).
- Meta fields: `id, name, crop, crop_name, growth_habit`.

### Views

`views/variety.py` (all `CustomAuthentication` + `IsAuthenticated`; `get_queryset` filters `crop__user=request.user`):

- `VarietyListApiView` (list + create): `SearchFilter` on `name`; `get`/`post`.
- `VarietyDetailAPIView` (retrieve/update/destroy): `get`/`put`/`patch`/`delete`.

Tag `"Variety"` on all schema decorators.

### URLs

`urls/variety.py` (mounted at `api/{API_VERSION}/varieties/`):

- `""` -> `VarietyListApiView` (`variety-list-create`).
- `"<int:pk>"` -> `VarietyDetailAPIView` (`variety-detail`).

### OpenAPI

`openapi/variety/`: `examples.py`, `parameters.py` (`VARIETY_ID_PARAM`), `responses.py`, `schemas.py`.

### Tests

`tests/variety.py` classes (all re-exported in `tests/__init__.py`):

- `VarietyListApiViewTests`, `VarietyCreateApiViewTests`, `VarietyGetApiViewTests`, `VarietyUpdateApiViewTests`, `VarietyPartialUpdateApiViewTests`, `VarietyDeleteApiViewTests`.

Factory: `VarietyFactory` in `tests/commons/factories.py`.

## Frontend (`frontend/src/`)

### View

`views/varieties/index.vue` (`VarietiesView`). Manages search (debounced 500ms), pagination, create/update dialogs, delete. Composes `VarietyCreateDialog`, `VarietyUpdateDialog`, `VarietiesTable`.

### Components

`components/varieties/`:

- `VarietiesTable.vue` (wraps `BaseDataTable`).
- `VarietyColumns.ts` (columns `name`, `cropName` "Crop", `growthHabit` badges, `actions`).
- `VarietyCreateDialog.vue` / `VarietyUpdateDialog.vue` (crop select fed by `useCrop`, growth-habit checkboxes).
- `VarietyTableActions.vue`.

### Composable

`composables/useVarieties.ts` -> `useVarieties(pagination?, searchTerm?)`.

- Query key `["varieties", pagination, "search"]`; `varietyService.getAll`.
- Mutations invalidate `["varieties"]`; re-throw `AxiosError<APIErrorResponse>`.

### API service

`api/services/varietyService.ts` -> `varietyService` (`getAll`/`create`/`update`/`delete`).

### Schema & types

- `schemas/variety.schemas.ts`: `GrowthHabitEnum`, `varietySchema` (`name`, `crop` coerced number, `growthHabit` array min 1).
- `types/variety.ts`: `Variety` (`id, name, crop, cropName, growthHabit`), `VarietyPayload`.

### Tests

`tests/views/varietiesView.spec.ts`, `tests/composables/useVarieties.spec.ts`, `tests/api/services/varietyService.spec.ts`, `tests/schemas/variety.schemas.spec.ts`, and `tests/components/varieties/*` (columns, create dialog, update dialog, table actions, table).

## Conventions & gotchas

- `growth_habit` is a multi-select array (Postgres ArrayField); frontend renders one badge per habit.
- `created_at` uses `auto_now=True` (updates on every save), a known quirk.
- Variety also appears as an FK on `Planting` and in `types/planting.ts` (`variety`/`varietyName`); that is the Plantings section.
