<script setup lang="ts">
import BaseDataTable from "@/components/BaseDataTable.vue"
import type { Variety } from "@/types/variety"
import { columns } from "./VarietyColumns"
import type { PaginationState } from "@/types/pagination"

const searchTerm = defineModel<string>("searchTerm", { default: "" })

defineProps<{
  data: Variety[]
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
