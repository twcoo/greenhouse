<script setup lang="ts">
import BaseDataTable from "@/components/BaseDataTable.vue"
import type { Planting } from "@/types/planting"
import { columns } from "./PlantingColumns"
import type { PaginationState } from "@/types/pagination"

const searchTerm = defineModel<string>("searchTerm", { default: "" })

defineProps<{
  data: Planting[]
  rowCount: number
  pagination: PaginationState
}>()
</script>

<template>
  <BaseDataTable
    v-model:searchTerm="searchTerm"
    :tableData="data"
    :columns="columns"
    :rowCount="rowCount"
    :pagination="pagination"
  />
</template>
