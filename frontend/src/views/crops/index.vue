<script setup lang="ts">
import { ref } from "vue"
import AppLayout from "@/layouts/AppLayout.vue"
import CropsTable from "@/components/crops/CropsTable.vue"
import CropsDialog from "@/components/crops/CropsDialog.vue"
import { useCrop } from "@/composables/useCrops"
import type { cropPayload } from "@/types/crop"

const pagination = ref({ pageIndex: 0, pageSize: 10 })

const { isLoading, createCrop, crops } = useCrop(pagination)

function handlePaginationChange(newState: { pageIndex: number; pageSize: number }) {
  console.log(pagination.value)
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

    <div v-if="isLoading && !crops" class="flex justify-center py-10">
      <p>Loading crops...</p>
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
