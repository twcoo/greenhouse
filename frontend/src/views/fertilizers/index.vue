<script setup lang="ts">
import { ref } from "vue"
import { watchDebounced } from "@vueuse/core"
import AppLayout from "@/layouts/AppLayout.vue"
import FertilizersTable from "@/components/fertilizers/FertilizersTable.vue"
import FertilizerCreateDialog from "@/components/fertilizers/FertilizerCreateDialog.vue"
import FertilizerUpdateDialog from "@/components/fertilizers/FertilizerUpdateDialog.vue"
import FertilizerLogSheet from "@/components/fertilizers/logs/FertilizerLogSheet.vue"
import { useFertilizers } from "@/composables/useFertilizers"
import { IconLoader2, IconPlus } from "@tabler/icons-vue"
import type { FertilizerPayload, Fertilizer } from "@/types/fertilizer"
import type { fertilizerForm } from "@/schemas/fertilizer.schemas"
import Button from "@/components/ui/button/Button.vue"

// Search Refs
const searchTerm = ref<string>("")

// Pagination Refs
const pagination = ref({ pageIndex: 0, pageSize: 10 })

// Create Fertilizer Refs
const openCreateDialog = ref<boolean>(false)

// Update Fertilizer Refs
const openUpdateDialog = ref<boolean>(false)
const fertilizerIdToUpdate = ref<number>(0)
const fertilizerUpdateFormState = ref<fertilizerForm | null>(null)

// Log Sheet Refs
const openLogSheet = ref<boolean>(false)
const fertilizerForLogs = ref<Fertilizer | null>(null)

// Fertilizer Composable
const {
  fertilizers,
  isLoading,
  isCreateSuccess,
  isUpdateSuccess,
  createFertilizer,
  updateFertilizer,
  deleteFertilizer,
  fetchFertilizers,
} = useFertilizers(pagination, searchTerm)

const handlePaginationChange = (newState: { pageIndex: number; pageSize: number }): void => {
  pagination.value = newState
}

const setUpdateDialog = async (id: number, data: unknown): Promise<void> => {
  fertilizerIdToUpdate.value = id
  fertilizerUpdateFormState.value = data as fertilizerForm
  openUpdateDialog.value = true
}

const handleCreateFertilizer = async (
  payload: FertilizerPayload,
  onError: (err: unknown) => void,
): Promise<void> => {
  try {
    await createFertilizer(payload)
  } catch (err) {
    onError(err)
  }
}

const handleUpdateFertilizer = async (
  id: number,
  payload: FertilizerPayload,
  onError: (err: unknown) => void,
): Promise<void> => {
  try {
    await updateFertilizer({ id, payload })
  } catch (err) {
    onError(err)
  }
}

const handleDeleteFertilizer = async (id: number): Promise<void> => {
  await deleteFertilizer(id)
  pagination.value = { ...pagination.value, pageIndex: 0 }
}

const handleManageLogs = (id: number): void => {
  fertilizerForLogs.value = fertilizers.value?.results.find((f) => f.id === id) ?? null
  openLogSheet.value = true
}

watchDebounced(
  searchTerm,
  () => {
    fetchFertilizers()
  },
  { debounce: 500 },
)
</script>

<template>
  <AppLayout>
    <!-- Create Fertilizer Dialog -->
    <div class="flex justify-end w-full mb-4">
      <Button @click="openCreateDialog = true" variant="outline">
        <IconPlus />
        <span class="hidden lg:inline">Add Fertilizer</span>
      </Button>
      <FertilizerCreateDialog
        v-model:open="openCreateDialog"
        :isLoading="isLoading"
        :isCreateSuccess="isCreateSuccess"
        @submit="handleCreateFertilizer"
      />
    </div>

    <!-- Update Fertilizer Dialog -->
    <FertilizerUpdateDialog
      v-if="fertilizerUpdateFormState"
      v-model:open="openUpdateDialog"
      :id="fertilizerIdToUpdate"
      :fertilizerFormInitialState="fertilizerUpdateFormState"
      :isLoading="isLoading"
      :isUpdateSuccess="isUpdateSuccess"
      @submit="handleUpdateFertilizer"
    />

    <!-- Fertilizers Table -->
    <div
      v-if="isLoading && !fertilizers?.results?.length"
      class="fixed inset-0 flex flex-col items-center justify-center bg-white/50"
    >
      <IconLoader2 class="animate-spin h-10 w-10 mb-2" />
      <span>Fetching fertilizers...</span>
    </div>

    <FertilizersTable
      v-else-if="fertilizers"
      :data="fertilizers.results"
      :rowCount="fertilizers.count"
      v-model:searchTerm="searchTerm"
      :pagination="pagination"
      @pagination-change="handlePaginationChange"
      @delete="handleDeleteFertilizer"
      @update="setUpdateDialog"
      @action="
        (name: string, id: number) => {
          if (name === 'manage-logs') handleManageLogs(id)
        }
      "
    />

    <!-- Fertilizer Log Sheet -->
    <FertilizerLogSheet
      v-if="fertilizerForLogs"
      v-model:open="openLogSheet"
      :fertilizerId="fertilizerForLogs.id"
      :fertilizer="fertilizerForLogs"
    />
  </AppLayout>
</template>
