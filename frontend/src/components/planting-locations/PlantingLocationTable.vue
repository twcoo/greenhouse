<script setup lang="ts">
import BaseDataTable from "@/components/BaseDataTable.vue"
import type { PlantingLocation } from "@/types/plantingLocation"
import { columns } from "./PlantingLocationColumns"
import type { PaginationState } from "@/types/pagination"

const searchTerm = defineModel<string>("searchTerm", { default: "" })

defineProps<{
  data: PlantingLocation[]
  rowCount: number
  pagination: PaginationState
}>()
</script>

<template>
  <BaseDataTable
    v-model:searchTerm="searchTerm"
    :tableData="data"
    :columns="columns"
    :filterableColumns="['locationType']"
    :rowCount="rowCount"
    :pagination="pagination"
  />
</template>
