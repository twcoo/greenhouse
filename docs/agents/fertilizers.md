# Fertilizers

## Overview

Full-stack management of fertilizer batches and their logs. Backend has a parent/child relationship: `Fertilizer` at `api/{API_VERSION}/fertilizers/` and `FertilizerLog` nested at `api/{API_VERSION}/fertilizers/<fertilizer_pk>/logs/`. Frontend route is `/fertilizers`.

## Backend (`backend/greenhouse/`)

### Models

`models/fertilizer.py` -> `Fertilizer`

- `user` FK (`related_name="fertilizers"`, CASCADE).
- `name` (100).
- `type` (TYPE_CHOICES: SWAMP / COMPOST / OTHER; default SWAMP).
- `status` (STATUS_CHOICES: BREWING / READY / USED / DISCARDED; default BREWING).
- `start_date` (default today), `ingredients` (ArrayField, default list).
- `log_added_ingredients` (ArrayField, internal bookkeeping, NOT exposed by serializer).
- `notes`, `created_at`/`updated_at`. Meta `ordering = ["-created_at"]`.

`models/fertilizer_log.py` -> `FertilizerLog`

- `fertilizer` FK (`related_name="logs"`, CASCADE).
- `event_type` (ADDED_INGREDIENT / ADDED_WATER / STIRRED / OTHER; default OTHER).
- `item_added` (100), `quantity` (50), `notes`, `log_date` (default today), timestamps.
- Meta `ordering = ["-log_date", "-pk"]`.

### Serializers

- `serializers/fertilizer.py` -> `FertilizerSerializer`: `id, name, type, status, start_date, ingredients, notes, created_at, updated_at` (`log_added_ingredients` intentionally omitted).
- `serializers/fertilizer_log.py` -> `FertilizerLogSerializer`: `id, event_type, item_added, quantity, notes, log_date, created_at, updated_at` (`fertilizer` FK resolved from URL).

### Views

`views/fertilizer.py` (all `CustomAuthentication` + `IsAuthenticated`, scope to `request.user`):

- `FertilizerListApiView` (list + create): `SearchFilter` on `name`.
- `FertilizerDetailApiView` (retrieve/update/destroy): `perform_update` prunes `log_added_ingredients` no longer in `ingredients` (casefold compare).

`views/fertilizer_log.py` (module helpers `_normalize_ingredient`, `_add_ingredient`, `_remove_ingredient_if_unreferenced` reconcile `ingredients` and `log_added_ingredients` on log create/update/delete):

- `FertilizerLogListApiView` (list + create): `_get_fertilizer` via `get_object_or_404(..., user=request.user)`; `perform_create` calls `_add_ingredient` when `event_type == "ADDED_INGREDIENT"`.
- `FertilizerLogDetailApiView` (update/destroy only, no retrieve).

### URLs

- `urls/fertilizer.py`: `""` (`fertilizer-list-create`), `"<int:pk>"` (`fertilizer-detail`), `"<int:fertilizer_pk>/logs/"` (include `fertilizer_log`).
- `urls/fertilizer_log.py`: `""` (`fertilizer-log-list-create`), `"<int:pk>"` (`fertilizer-log-detail`).

### OpenAPI

`openapi/fertilizer/` and `openapi/fertilizer_log/`.

### Tests

- `tests/fertilizer.py`: `FertilizerListApiViewTests`, `FertilizerCreateApiViewTests`, `FertilizerGetApiViewTests`, `FertilizerUpdateApiViewTests`, `FertilizerDeleteApiViewTests`, `FertilizerLogCascadeTests`.
- `tests/fertilizer_log.py`: `FertilizerLogListApiViewTests`, `FertilizerLogCreateApiViewTests`, `FertilizerLogDetailApiViewTests`.

Discovery gotcha: `tests/__init__.py` does not re-export the fertilizer/fertilizer_log test classes, so they will silently not run until added there.

Factories: `FertilizerFactory`, `FertilizerLogFactory`.

## Frontend (`frontend/src/`)

### View

`views/fertilizers/index.vue` (`FertilizersView`). Manages search (debounced 500ms), pagination, create/update dialogs, delete, and the log sheet (`manage-logs` action).

### Components

`components/fertilizers/`:

- `FertilizersTable.vue`, `FertilizerColumns.ts` (name/type/status/startDate/ingredients/actions), `FertilizerTableActions.vue` (Update / Logs / Delete).
- `FertilizerCreateDialog.vue`, `FertilizerUpdateDialog.vue` (ingredients chip input with dedupe).

Missing: `views/fertilizers/index.vue` imports `@/components/fertilizers/logs/FertilizerLogSheet.vue`, but no such file exists. The log data layer (`useFertilizerLogs`, `fertilizerLogService`, `fertilizerLogSchema`, types, tests) is implemented, but the log sheet UI component is absent (stubbed in tests). This will fail `vue-tsc` build.

### Composables

- `composables/useFertilizers.ts` -> `useFertilizers(pagination?, searchTerm?)`; key `["fertilizers", pagination, "search"]`; mutations invalidate `["fertilizers"]`.
- `composables/useFertilizerLogs.ts` -> `useFertilizerLogs(fertilizerId, pagination?)`; key `["fertilizer-logs", fertilizerId, pagination]`; mutations invalidate `["fertilizer-logs", fertilizerId]` and `["fertilizers"]`.

### API services

- `fertilizerService.ts` (`getAll`/`create`/`update`/`delete` on `/fertilizers/`).
- `fertilizerLogService.ts` (nested under `/fertilizers/${fertilizerId}/logs/`).

### Schemas & types

- `schemas/fertilizer.schemas.ts` (`FERTILIZER_TYPES`, `FERTILIZER_STATUSES`, `fertilizerSchema`).
- `schemas/fertilizerLog.schemas.ts` (`FERTILIZER_LOG_EVENT_TYPES`, `fertilizerLogSchema`).
- `types/fertilizer.ts`, `types/fertilizerLog.ts`.

### Tests

`tests/views/fertilizersView.spec.ts`, `tests/composables/useFertilizers.spec.ts`, `tests/composables/useFertilizerLogs.spec.ts`, service specs, schema specs, and component specs under `tests/components/fertilizers/`.

## Conventions & gotchas

- `Fertilizer.log_added_ingredients` is hidden server-side bookkeeping to distinguish log-added ingredients from manual edits; reconciled by `FertilizerDetailApiView.perform_update` and the log views using casefold-insensitive comparison.
- Logs are always resolved through the parent fertilizer scoped to the user; cross-user access returns 404.
- Missing `FertilizerLogSheet.vue` component (see Components).
- Backend fertilizer tests not re-exported in `tests/__init__.py` (see Tests).
