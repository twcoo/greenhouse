<script setup lang="ts">
import BaseDataTable from "@/components/BaseDataTable.vue"
import type { Crop } from "@/types/crop"
import { columns } from "./CropColumns"
import type { PaginationState } from "@/types/pagination"

const searchTerm = defineModel<string>("searchTerm", { default: "" })

defineProps<{
  data: Crop[]
  rowCount: number
  pagination: PaginationState
}>()
</script>

<template>
  <BaseDataTable
    v-model:searchTerm="searchTerm"
    :tableData="data"
    :columns="columns"
    :filterableColumns="['category', 'sunlightRequirement']"
    :rowCount="rowCount"
    :pagination="pagination"
  />
</template>
