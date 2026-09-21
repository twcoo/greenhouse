<script setup lang="ts">
import BaseDataTable from "@/components/BaseDataTable.vue"
import type { Fertilizer } from "@/types/fertilizer"
import { columns } from "./FertilizerColumns"
import type { PaginationState } from "@/types/pagination"

const searchTerm = defineModel<string>("searchTerm", { default: "" })

defineProps<{
  data: Fertilizer[]
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
