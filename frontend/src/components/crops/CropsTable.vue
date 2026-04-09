<script setup lang="ts">
import BaseDataTable from "@/components/BaseDataTable.vue"
import type { Crop } from "@/types/crop"
import { columns } from "./CropColumns"
import type { PaginationState } from "@/types/pagination"

defineProps<{
  data: Crop[]
  rowCount: number
  pagination: PaginationState
}>()
</script>

<template>
  <BaseDataTable
    :tableData="data"
    :columns="columns"
    :filterableColumns="['category', 'sunlightRequirement']"
    :rowCount="rowCount"
    :pagination="pagination"
  />
</template>
