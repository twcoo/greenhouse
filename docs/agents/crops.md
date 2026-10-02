# Crops

## Overview

Full-stack CRUD for crops at `api/{API_VERSION}/crops/` (backend) and `/crops` (frontend, route `crops`). Crops are user-owned; varieties and plantings reference them by foreign key.

## Backend (`backend/greenhouse/`)

### Model

`models/crop.py` -> `Crop`

- `user` FK -> `User` (`related_name="crops"`, CASCADE).
- `name` (50, `unique=True`), `scientific_name` (100, `unique=True`).
- `category` (15, `CATEGORY_CHOICES` = VEGETABLE / FRUIT).
- `sunlight_requirement` (15, `SUNLIGHT_REQUIREMENT_CHOICES` = FULL SUN / PART SUN / FULL SHADE).
- `min_days_to_harvest`, `max_days_to_harvest` (IntegerField).
- `image` (ImageField `upload_to="crops/"`, nullable).
- `created_at` (auto_now_add), `updated_at` (auto_now).
- Meta: `ordering = ["-created_at"]`; indexes `crop_user_created_idx` and trigram `GinIndex` on `name` and `scientific_name`.

### Serializer

`serializers/crops.py`

- `CropSerializer` (decorated `@extend_schema_serializer`). Exposes `id, name, scientific_name, category, sunlight_requirement, min_days_to_harvest, max_days_to_harvest` (image/user/timestamps are NOT exposed).
  - Per-field `UniqueValidator` on name/scientific_name + `UniqueTogetherValidator`.
  - `validate_name`/`validate_scientific_name` reject digit-only values.
  - `validate` enforces `min_days_to_harvest <= max_days_to_harvest`.
- `CropImageSerializer` inherits `UploadImageSerializer` from `serializers/utils.py` (validates `.jpg`/`.jpeg`/`.png`, 2 MB max).

### Views

`views/crops.py` (all `CustomAuthentication` + `IsAuthenticated`, all scope to `request.user`):

- `CropListAPIView` (list + create): `SearchFilter` on `name`/`scientific_name`; `perform_create` sets `user`. `get`/`post`.
- `CropDetailAPIView` (retrieve/update/destroy): `get`/`put`/`patch`/`delete`.
- `CropUploadImageAPIView` (`put` only): `MultiPartParser`/`FormParser`, uses `CropImageSerializer`.

All decorated with `@extend_schema`/`@extend_schema_view` under tag `"Crop"`.

### URLs

`urls/crops.py` (mounted at `api/{API_VERSION}/crops/`):

- `""` -> `CropListAPIView` (`crop-list-create`).
- `"<int:pk>"` -> `CropDetailAPIView` (`crop-detail`).
- `"<int:pk>/image/"` -> `CropUploadImageAPIView` (`crop-image-upload`).

### OpenAPI

`openapi/crop/` (singular): `examples.py`, `parameters.py` (`CROP_ID_PARAM`), `responses.py`, `schemas.py` (`CROP_RESPONSE_DATA_SCHEMA`).

### Tests

`tests/crops.py` classes (all re-exported in `tests/__init__.py`):

- `CropListApiViewTests`, `CropCreateApiViewTests`, `CropGetApiViewTests`, `CropUpdateApiViewTests`, `CropPartialUpdateApiViewTests`, `CropDeleteApiViewTests`, `CropImageUploadApiViewTests`.

Factory: `CropFactory` in `tests/commons/factories.py`.

## Frontend (`frontend/src/`)

### View

`views/crops/index.vue` (`CropsView`). Manages search (debounced 500ms), pagination, create/update dialogs, delete (resets pageIndex). Composes `CropCreateDialog`, `CropUpdateDialog`, `CropsTable`.

### Components

`components/crops/`:

- `CropsTable.vue` (wraps `BaseDataTable`, filterable columns `category`/`sunlightRequirement`).
- `CropColumns.ts` (TanStack `ColumnDef<Crop>[]`).
- `CropCreateDialog.vue` / `CropUpdateDialog.vue` (zod-validated forms).
- `CropTableActions.vue` (row dropdown + delete confirm).

### Composable

`composables/useCrops.ts` -> `useCrop(pagination?, searchTerm?)`.

- Query key `["crops", pagination, "search"]`; `cropService.getAll`.
- Mutations `createCrop`/`updateCrop`/`deleteCrop` invalidate `["crops"]`; re-throw `AxiosError`.

### API service

`api/services/cropsService.ts` -> `cropService` (`getAll`/`create`/`update`/`delete` on `/crops/`).

### Schema & types

- `schemas/crops.schemas.ts`: `CategoryEnum`, `SunlightRequirementEnum`, `cropsSchema` (with `.refine` max >= min days).
- `types/crop.ts`: `Crop`, `cropPayload`.

### Tests

`tests/views/cropsView.spec.ts`, `tests/api/services/cropsService.spec.ts`, `tests/composables/useCrops.spec.ts`, `tests/schemas/crops.schemas.spec.ts`, and `tests/components/crops/*` (create dialog, update dialog, table, columns, table actions).

## Conventions & gotchas

- Image is managed by a separate `PUT /crops/<id>/image/` endpoint; the frontend does not implement image upload/display.
- Uniqueness enforced at DB level + `UniqueValidator` + `UniqueTogetherValidator`; search is trigram-accelerated.
- Cross-user access returns 404 (not 403) because querysets are user-scoped.
- Detail URL path has no trailing slash (`<int:pk>`).
