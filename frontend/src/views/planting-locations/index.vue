<script setup lang="ts">
import { ref } from "vue"
import { watchDebounced } from "@vueuse/core"
import AppLayout from "@/layouts/AppLayout.vue"
import PlantingLocationTable from "@/components/planting-locations/PlantingLocationTable.vue"
import PlantingLocationCreateDialog from "@/components/planting-locations/PlantingLocationCreateDialog.vue"
import PlantingLocationUpdateDialog from "@/components/planting-locations/PlantingLocationUpdateDialog.vue"
import PlantingLocationStatusSheet from "@/components/planting-locations/status/PlantingLocationStatusSheet.vue"
import { usePlantingLocations } from "@/composables/usePlantingLocations"
import { IconLoader2, IconPlus } from "@tabler/icons-vue"
import type { PlantingLocationPayload } from "@/types/plantingLocation"
import type { PlantingLocationForm } from "@/schemas/plantingLocation.schemas"
import type { PlantingLocationStatus } from "@/types/plantingLocationStatus"
import Button from "@/components/ui/button/Button.vue"

// Search Refs
const searchTerm = ref<string>("")

// Pagination Refs
const pagination = ref({ pageIndex: 0, pageSize: 10 })

// Create Location Refs
const openCreateDialog = ref<boolean>(false)

// Update Location Refs
const openUpdateDialog = ref<boolean>(false)
const locationIdToUpdate = ref<number>(0)
const locationUpdateFormState = ref<PlantingLocationForm | null>(null)

// Status Sheet Refs
const openStatusSheet = ref<boolean>(false)
const locationIdForStatus = ref<number | null>(null)
const currentStatusForStatus = ref<PlantingLocationStatus | null>(null)

// Location Composable
const {
  locations,
  isLoading,
  isCreateSuccess,
  isUpdateSuccess,
  createLocation,
  updateLocation,
  deleteLocation,
  fetchLocations,
} = usePlantingLocations(pagination, searchTerm)

const handlePaginationChange = (newState: { pageIndex: number; pageSize: number }): void => {
  pagination.value = newState
}

const setUpdateDialog = async (id: number, location: PlantingLocationForm): Promise<void> => {
  locationIdToUpdate.value = id
  locationUpdateFormState.value = location
  openUpdateDialog.value = true
}

const handleCreateLocation = async (
  payload: PlantingLocationPayload,
  onError: (err: unknown) => void,
): Promise<void> => {
  try {
    await createLocation(payload)
  } catch (err) {
    onError(err)
  }
}

const handleUpdateLocation = async (
  id: number,
  payload: PlantingLocationPayload,
  onError: (err: unknown) => void,
) => {
  try {
    await updateLocation({ id, payload })
  } catch (err) {
    onError(err)
  }
}

const handleDeleteLocation = async (id: number): Promise<void> => {
  await deleteLocation(id)
  pagination.value = { ...pagination.value, pageIndex: 0 }
}

const handleTableAction = (name: string, id: number): void => {
  if (name === "manage-status") {
    const location = locations.value?.results.find((l) => l.id === id)
    locationIdForStatus.value = id
    currentStatusForStatus.value = location?.currentStatus ?? null
    openStatusSheet.value = true
  }
}

watchDebounced(
  searchTerm,
  () => {
    fetchLocations()
  },
  { debounce: 500 },
)
</script>

<template>
  <AppLayout>
    <!-- Create Location Dialog -->
    <div class="flex justify-end w-full mb-4">
      <Button @click="openCreateDialog = true" variant="outline">
        <IconPlus />
        <span class="hidden lg:inline">Add Location</span>
      </Button>
      <PlantingLocationCreateDialog
        v-model:open="openCreateDialog"
        :isLoading="isLoading"
        :isCreateSuccess="isCreateSuccess"
        @submit="handleCreateLocation"
      />
    </div>

    <!-- Update Location Dialog -->
    <PlantingLocationUpdateDialog
      v-if="locationUpdateFormState"
      v-model:open="openUpdateDialog"
      :id="locationIdToUpdate"
      :locationFormInitialState="locationUpdateFormState"
      :isLoading="isLoading"
      :isUpdateSuccess="isUpdateSuccess"
      @submit="handleUpdateLocation"
    >
    </PlantingLocationUpdateDialog>

    <!-- Status Sheet -->
    <PlantingLocationStatusSheet
      v-if="locationIdForStatus"
      :key="locationIdForStatus"
      v-model:open="openStatusSheet"
      :locationId="locationIdForStatus"
      :currentStatus="currentStatusForStatus"
    />

    <!-- Locations Table -->
    <div
      v-if="isLoading && !locations?.results?.length"
      class="fixed inset-0 flex flex-col items-center justify-center bg-white/50"
    >
      <IconLoader2 class="animate-spin h-10 w-10 mb-2" />
      <span>Fetching locations...</span>
    </div>

    <PlantingLocationTable
      v-else-if="locations"
      :data="locations.results"
      :rowCount="locations.count"
      v-model:searchTerm="searchTerm"
      :pagination="pagination"
      @pagination-change="handlePaginationChange"
      @delete="handleDeleteLocation"
      @update="setUpdateDialog"
      @action="handleTableAction"
    />
  </AppLayout>
</template>
