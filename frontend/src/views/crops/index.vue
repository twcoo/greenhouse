<script setup lang="ts">
import { ref } from "vue"
import AppLayout from "@/layouts/AppLayout.vue"
import CropsTable from "@/components/crops/CropsTable.vue"
import CropCreateDialog from "@/components/crops/CropCreateDialog.vue"
import { useCrop } from "@/composables/useCrops"
import { IconLoader2, IconPlus } from "@tabler/icons-vue"
import type { cropPayload } from "@/types/crop"
import Button from "@/components/ui/button/Button.vue"

const pagination = ref({ pageIndex: 0, pageSize: 10 })
const openCreateDialog = ref<boolean>(false)

const { isLoading, createError, createCrop, crops, deleteCrop } = useCrop(pagination)

function handlePaginationChange(newState: { pageIndex: number; pageSize: number }) {
  pagination.value = newState
}

async function handleCreateCrop(payload: cropPayload, onError: (err: any) => void): Promise<void> {
  try {
    await createCrop(payload)
  } catch (err) {
    onError(err)
  }
}

async function handleDeleteCrop(id): Promise<void> {
  await deleteCrop(id)
}
</script>

<template>
  <AppLayout>
    <div class="flex justify-end w-full mb-4">
      <Button @click="openCreateDialog = true" variant="outline">
        <IconPlus />
        <span class="hidden lg:inline">Add Crop</span>
      </Button>
      <CropCreateDialog
        v-model:open="openCreateDialog"
        :isLoading="isLoading"
        :isError="createError"
        @submit="handleCreateCrop"
      />
    </div>
    <div v-if="isLoading" class="flex items-center justify-center gap-2">
      <IconLoader2 :size="18" class="animate-spin" />
      <span>Fetching crops...</span>
    </div>
    <CropsTable
      v-else
      :data="crops.results"
      :rowCount="crops.count"
      :pagination="pagination"
      @pagination-change="handlePaginationChange"
      @delete="handleDeleteCrop"
    />
  </AppLayout>
</template>
