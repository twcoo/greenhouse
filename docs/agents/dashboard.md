# Dashboard

## Overview

Read-only aggregation view at `/dashboard` (route name `dashboard`, `meta.requiresAuth`). It has no backend entity of its own; it reads the Plantings and Planting Locations APIs and derives summary stats client-side.

## Frontend

### View

- `frontend/src/views/dashboard/index.vue` (default export `DashboardView`, `<script setup>`).
- Wrapped in `AppLayout` (which renders `AppSidebar` and `SiteHeader`).

Data pulled via composables (each requested with a wide `pageSize: 100`):

- `usePlantings({ pageIndex: 0, pageSize: 100 })` -> `plantings`.
- `usePlantingLocations({ pageIndex: 0, pageSize: 100 })` -> `locations`.

Derived computed values:

- `totalPlantings` = `plantings.value?.count ?? 0`.
- `totalLocations` = `locations.value?.count ?? 0`.
- `locationResults` = `locations.value?.results ?? []`.
- `inUseCount` = locations where `currentStatus?.status === "IN_USE"`.
- `availableCount` = locations where `!currentStatus || currentStatus.status === "AVAILABLE"` (null status counts as available).
- `recentPlantings` = `plantings.results` sorted by `createdAt` descending, sliced to 5.

Rendered sections:

- "Plantings": "Total Plantings" stat card + "Recent Plantings" table (columns Crop, Variety, Added) with empty state "No plantings yet." and a `RouterLink` "View all" to `/plantings`.
- "Planting Locations": "Total Locations", "In Use", "Available" stat cards + "Location Overview" table (columns Name, Type, Status) with empty state "No locations yet." and a "View all" link to `/planting-locations`.

Module-level label maps in the view:

- `LOCATION_TYPE_LABEL`: `NURSERYPOT` -> "Nursery Pot", `POT` -> "Pot", `GROUND` -> "Ground".
- `STATUS_LABEL`: `AVAILABLE` -> "Available", `IN_USE` -> "In Use", `DAMAGED` -> "Damaged", `DESTROYED` -> "Destroyed", `RETIRED` -> "Retired".
- `STATUS_BADGE_VARIANT`: `AVAILABLE` -> `secondary`, `IN_USE` -> `default`, `DAMAGED`/`DESTROYED` -> `destructive`, `RETIRED` -> `outline`.

### Dependencies

- Composables: `usePlantings` (`frontend/src/composables/usePlantings.ts`), `usePlantingLocations` (`frontend/src/composables/usePlantingLocations.ts`).
- Services (consumed indirectly): `plantingService.getAll`, `plantingLocationService.getAll`.
- Util: `formatDate` (`frontend/src/utils/formatting.ts`).
- Types: `Planting`, `PlantingLocation`, `PlantingLocationStatus`, `PaginatedResponse<T>`.

No Pinia store is used directly; no create/update/delete operations.

### Tests

- `frontend/src/tests/views/dashboardView.spec.ts` (the dedicated dashboard spec; mocks `usePlantings`/`usePlantingLocations`, asserts section headings, stat counts, recent-plantings sort/limit, empty states, and "View all" links).
- Route/nav references in `tests/router/router.spec.ts`, `tests/components/appSideBar.spec.ts`, `tests/components/navMain.spec.ts`, `tests/components/login/loginForm.spec.ts`, `tests/components/setup/setupAdminForm.spec.ts`.

## Conventions & gotchas

- Always requests `pageSize: 100` and derives summaries client-side.
- The location status badge logic treats a `null` `currentStatus` as "Available".
- If the Plantings or Planting Locations sections change shape, this view's computed fields and label maps must be revisited.
