<script setup lang="ts">
import { ref } from "vue"
import { watchDebounced } from "@vueuse/core"
import AppLayout from "@/layouts/AppLayout.vue"
import VarietiesTable from "@/components/varieties/VarietiesTable.vue"
import VarietyCreateDialog from "@/components/varieties/VarietyCreateDialog.vue"
import VarietyUpdateDialog from "@/components/varieties/VarietyUpdateDialog.vue"
import { useVarieties } from "@/composables/useVarieties"
import { IconLoader2, IconPlus } from "@tabler/icons-vue"
import type { VarietyPayload } from "@/types/variety"
import type { varietyForm } from "@/schemas/variety.schemas"
import Button from "@/components/ui/button/Button.vue"

// Search Refs
const searchTerm = ref<string>("")

// Pagination Refs
const pagination = ref({ pageIndex: 0, pageSize: 10 })

// Create Variety Refs
const openCreateDialog = ref<boolean>(false)

// Update Variety Refs
const openUpdateDialog = ref<boolean>(false)
const varietyIdToUpdate = ref<number>(0)
const varietyUpdateFormState = ref<varietyForm | null>(null)

// Variety Composable
const {
  varieties,
  isLoading,
  isCreateSuccess,
  isUpdateSuccess,
  createVariety,
  updateVariety,
  deleteVariety,
  fetchVarieties,
} = useVarieties(pagination, searchTerm)

const handlePaginationChange = (newState: { pageIndex: number; pageSize: number }): void => {
  pagination.value = newState
}

const setUpdateDialog = async (id: number, variety: varietyForm): Promise<void> => {
  varietyIdToUpdate.value = id
  varietyUpdateFormState.value = variety
  openUpdateDialog.value = true
}

const handleCreateVariety = async (
  payload: VarietyPayload,
  onError: (err: unknown) => void,
): Promise<void> => {
  try {
    await createVariety(payload)
  } catch (err) {
    onError(err)
  }
}

const handleUpdateVariety = async (
  id: number,
  payload: VarietyPayload,
  onError: (err: unknown) => void,
): Promise<void> => {
  try {
    await updateVariety({ id, payload })
  } catch (err) {
    onError(err)
  }
}

const handleDeleteVariety = async (id: number): Promise<void> => {
  await deleteVariety(id)
  pagination.value = { ...pagination.value, pageIndex: 0 }
}

watchDebounced(
  searchTerm,
  () => {
    fetchVarieties()
  },
  { debounce: 500 },
)
</script>

<template>
  <AppLayout>
    <!-- Create Variety Dialog -->
    <div class="flex justify-end w-full mb-4">
      <Button @click="openCreateDialog = true" variant="outline">
        <IconPlus />
        <span class="hidden lg:inline">Add Variety</span>
      </Button>
      <VarietyCreateDialog
        v-model:open="openCreateDialog"
        :isLoading="isLoading"
        :isCreateSuccess="isCreateSuccess"
        @submit="handleCreateVariety"
      />
    </div>

    <!-- Update Variety Dialog -->
    <VarietyUpdateDialog
      v-if="varietyUpdateFormState"
      v-model:open="openUpdateDialog"
      :id="varietyIdToUpdate"
      :varietyFormInitialState="varietyUpdateFormState"
      :isLoading="isLoading"
      :isUpdateSuccess="isUpdateSuccess"
      @submit="handleUpdateVariety"
    />

    <!-- Varieties Table -->
    <div
      v-if="isLoading && !varieties?.results?.length"
      class="fixed inset-0 flex flex-col items-center justify-center bg-white/50"
    >
      <IconLoader2 class="animate-spin h-10 w-10 mb-2" />
      <span>Fetching varieties...</span>
    </div>

    <VarietiesTable
      v-else-if="varieties"
      :data="varieties.results"
      :rowCount="varieties.count"
      v-model:searchTerm="searchTerm"
      :pagination="pagination"
      @pagination-change="handlePaginationChange"
      @delete="handleDeleteVariety"
      @update="setUpdateDialog"
    />
  </AppLayout>
</template>
