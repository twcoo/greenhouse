<script setup lang="ts">
import { ref } from "vue"
import AppLayout from "@/layouts/AppLayout.vue"
import CropsTable from "@/components/crops/CropsTable.vue"
import CropCreateDialog from "@/components/crops/CropCreateDialog.vue"
import CropUpdateDialog from "@/components/crops/CropUpdateDialog.vue"
import { useCrop } from "@/composables/useCrops"
import { IconLoader2, IconPlus } from "@tabler/icons-vue"
import type { cropPayload } from "@/types/crop"
import type { cropsForm } from "@/schemas/crops.schemas"
import Button from "@/components/ui/button/Button.vue"

const searchTerm = ref<string>("")

// Pagination Refs
const pagination = ref({ pageIndex: 0, pageSize: 10 })

// Create Crop Refs
const openCreateDialog = ref<boolean>(false)

// Update Crop Refs
const openUpdateDialog = ref<boolean>(false)
const cropIdToUpdate = ref<number>(0)
const cropUpdateFormState = ref<cropsForm | null>(null)

// Crop Composable
const { crops, isLoading, isCreateSuccess, isUpdateSuccess, createCrop, updateCrop, deleteCrop } =
  useCrop(pagination)

const handlePaginationChange = (newState: { pageIndex: number; pageSize: number }) => {
  pagination.value = newState
}

const setUpdateDialog = async (id: number, crop: cropsForm): Promise<void> => {
  cropIdToUpdate.value = id
  cropUpdateFormState.value = crop
  openUpdateDialog.value = true
}

const handleCreateCrop = async (
  payload: cropPayload,
  onError: (err: unknown) => void,
): Promise<void> => {
  try {
    await createCrop(payload)
  } catch (err) {
    onError(err)
  }
}

const handleUpdateCrop = async (
  id: number,
  payload: cropPayload,
  onError: (err: unknown) => void,
) => {
  try {
    await updateCrop({ id, payload })
  } catch (err) {
    onError(err)
  }
}

const handleDeleteCrop = async (id: number): Promise<void> => {
  await deleteCrop(id)
  pagination.value = { ...pagination.value, pageIndex: 0 }
}
</script>

<template>
  <AppLayout>
    <!-- Create Crop Dialog -->
    <div class="flex justify-end w-full mb-4">
      <Button @click="openCreateDialog = true" variant="outline">
        <IconPlus />
        <span class="hidden lg:inline">Add Crop</span>
      </Button>
      <CropCreateDialog
        v-model:open="openCreateDialog"
        :isLoading="isLoading"
        :isCreateSuccess="isCreateSuccess"
        @submit="handleCreateCrop"
      />
    </div>

    <!-- Update Crop Dialog -->
    <CropUpdateDialog
      v-if="cropUpdateFormState"
      v-model:searchTerm="searchTerm"
      v-model:open="openUpdateDialog"
      :id="cropIdToUpdate"
      :cropsFormInitialState="cropUpdateFormState"
      :isLoading="isLoading"
      :isUpdateSuccess="isUpdateSuccess"
      @submit="handleUpdateCrop"
    >
    </CropUpdateDialog>

    <!-- Crops Table -->
    <div v-if="isLoading && !crops?.results?.length">
      <IconLoader2 class="animate-spin" />
      <span>Fetching crops...</span>
    </div>

    <CropsTable
      v-else-if="crops"
      :data="crops.results"
      :rowCount="crops.count"
      :searchTerm="searchTerm"
      :pagination="pagination"
      @pagination-change="handlePaginationChange"
      @delete="handleDeleteCrop"
      @update="setUpdateDialog"
    />
  </AppLayout>
</template>
