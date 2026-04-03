<script setup lang="ts">
import { ref } from "vue"
import AppLayout from "@/layouts/AppLayout.vue"
import CropsTable from "@/components/crops/CropsTable.vue"
import CropsDialog from "@/components/crops/CropsDialog.vue"
import { useCrop } from "@/composables/useCrops"
import { IconLoader2 } from "@tabler/icons-vue"
import type { cropPayload } from "@/types/crop"

const pagination = ref({ pageIndex: 0, pageSize: 10 })

const { isLoading, createCrop, crops } = useCrop(pagination)

function handlePaginationChange(newState: { pageIndex: number; pageSize: number }) {
  pagination.value = newState
}

async function handleCreateCrop(payload: cropPayload): Promise<void> {
  await createCrop(payload)
}
</script>

<template>
  <AppLayout>
    <div class="flex justify-end w-full mb-4">
      <CropsDialog mode="create" :loading="isLoading" @submit="handleCreateCrop" />
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
    />
  </AppLayout>
</template>
