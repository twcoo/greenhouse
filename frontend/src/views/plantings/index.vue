<script setup lang="ts">
import { ref } from "vue"
import { watchDebounced } from "@vueuse/core"
import AppLayout from "@/layouts/AppLayout.vue"
import PlantingsTable from "@/components/plantings/PlantingsTable.vue"
import PlantingCreateDialog from "@/components/plantings/PlantingCreateDialog.vue"
import PlantingUpdateDialog from "@/components/plantings/PlantingUpdateDialog.vue"
import PlantingLocationAssignmentSheet from "@/components/planting-location-assignments/PlantingLocationAssignmentSheet.vue"
import PlantingDailyObservationSheet from "@/components/plantings/daily-observation/PlantingDailyObservationSheet.vue"
import { usePlantings } from "@/composables/usePlantings"
import { IconLoader2, IconPlus } from "@tabler/icons-vue"
import type { PlantingPayload } from "@/types/planting"
import type { plantingForm } from "@/schemas/planting.schemas"
import Button from "@/components/ui/button/Button.vue"

// Search Refs
const searchTerm = ref<string>("")

// Pagination Refs
const pagination = ref({ pageIndex: 0, pageSize: 10 })

// Create Planting Refs
const openCreateDialog = ref<boolean>(false)

// Update Planting Refs
const openUpdateDialog = ref<boolean>(false)
const plantingIdToUpdate = ref<number>(0)
const plantingUpdateFormState = ref<plantingForm | null>(null)

// Location Assignment Sheet Refs
const openLocationSheet = ref<boolean>(false)
const plantingIdForSheet = ref<number>(0)

// Daily Observation Sheet Refs
const openObservationSheet = ref<boolean>(false)
const plantingIdForObservations = ref<number>(0)

// Planting Composable
const {
  plantings,
  isLoading,
  isCreateSuccess,
  isUpdateSuccess,
  createPlanting,
  updatePlanting,
  deletePlanting,
  fetchPlantings,
} = usePlantings(pagination, searchTerm)

const handlePaginationChange = (newState: { pageIndex: number; pageSize: number }): void => {
  pagination.value = newState
}

const setUpdateDialog = async (id: number, planting: plantingForm): Promise<void> => {
  plantingIdToUpdate.value = id
  plantingUpdateFormState.value = planting
  openUpdateDialog.value = true
}

const handleCreatePlanting = async (
  payload: PlantingPayload,
  onError: (err: unknown) => void,
): Promise<void> => {
  try {
    await createPlanting(payload)
  } catch (err) {
    onError(err)
  }
}

const handleUpdatePlanting = async (
  id: number,
  payload: PlantingPayload,
  onError: (err: unknown) => void,
): Promise<void> => {
  try {
    await updatePlanting({ id, payload })
  } catch (err) {
    onError(err)
  }
}

const handleDeletePlanting = async (id: number): Promise<void> => {
  await deletePlanting(id)
  pagination.value = { ...pagination.value, pageIndex: 0 }
}

const handleManageLocations = (id: number): void => {
  plantingIdForSheet.value = id
  openLocationSheet.value = true
}

const handleDailyObservations = (id: number): void => {
  plantingIdForObservations.value = id
  openObservationSheet.value = true
}

watchDebounced(
  searchTerm,
  () => {
    fetchPlantings()
  },
  { debounce: 500 },
)
</script>

<template>
  <AppLayout>
    <!-- Create Planting Dialog -->
    <div class="flex justify-end w-full mb-4">
      <Button @click="openCreateDialog = true" variant="outline">
        <IconPlus />
        <span class="hidden lg:inline">Add Planting</span>
      </Button>
      <PlantingCreateDialog
        v-model:open="openCreateDialog"
        :isLoading="isLoading"
        :isCreateSuccess="isCreateSuccess"
        @submit="handleCreatePlanting"
      />
    </div>

    <!-- Update Planting Dialog -->
    <PlantingUpdateDialog
      v-if="plantingUpdateFormState"
      v-model:open="openUpdateDialog"
      :id="plantingIdToUpdate"
      :plantingFormInitialState="plantingUpdateFormState"
      :isLoading="isLoading"
      :isUpdateSuccess="isUpdateSuccess"
      @submit="handleUpdatePlanting"
    />

    <!-- Plantings Table -->
    <div
      v-if="isLoading && !plantings?.results?.length"
      class="fixed inset-0 flex flex-col items-center justify-center bg-white/50"
    >
      <IconLoader2 class="animate-spin h-10 w-10 mb-2" />
      <span>Fetching plantings...</span>
    </div>

    <PlantingsTable
      v-else-if="plantings"
      :data="plantings.results"
      :rowCount="plantings.count"
      v-model:searchTerm="searchTerm"
      :pagination="pagination"
      @pagination-change="handlePaginationChange"
      @delete="handleDeletePlanting"
      @update="setUpdateDialog"
      @action="
        (name: string, id: number) => {
          if (name === 'manage-locations') handleManageLocations(id)
          if (name === 'daily-observations') handleDailyObservations(id)
        }
      "
    />

    <!-- Location Assignment Sheet -->
    <PlantingLocationAssignmentSheet
      v-if="plantingIdForSheet"
      v-model:open="openLocationSheet"
      :plantingId="plantingIdForSheet"
    />

    <!-- Daily Observation Sheet -->
    <PlantingDailyObservationSheet
      v-if="plantingIdForObservations"
      v-model:open="openObservationSheet"
      :plantingId="plantingIdForObservations"
    />
  </AppLayout>
</template>
