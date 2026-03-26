<script setup lang="ts">
import BaseDataTable from "@/components/BaseDataTable.vue"
import { h } from "vue"
import type { ColumnDef } from "@tanstack/vue-table"

interface Crop {
  id: number
  name: string
  scientific_name: string
  category: string
  sunlight_requirement: string
  min_days_to_harvest: number
  max_days_to_harvest: number
}

// Column definitions with sorting and filtering enabled
const columns: ColumnDef<Crop>[] = [
  {
    accessorKey: "name",
    header: "Name",
    cell: ({ row }) => h("div", row.getValue("name")),
    enableSorting: true,
    enableFiltering: true,
  },
  {
    accessorKey: "scientific_name",
    header: "Scientific Name",
    cell: ({ row }) => h("div", row.getValue("scientific_name")),
    enableSorting: true,
    enableFiltering: true,
  },
  {
    accessorKey: "category",
    header: "Category",
    cell: ({ row }) => h("div", row.getValue("category")),
    enableSorting: true,
    enableFiltering: true,
  },
  {
    accessorKey: "sunlight_requirement",
    header: "Sunlight",
    cell: ({ row }) => h("div", row.getValue("sunlight_requirement")),
    enableSorting: true,
    enableFiltering: true,
  },
  {
    accessorKey: "min_days_to_harvest",
    header: "Min Days to Harvest",
    cell: ({ row }) => h("div", String(row.getValue("min_days_to_harvest"))),
    enableSorting: true,
    enableFiltering: true,
  },
  {
    accessorKey: "max_days_to_harvest",
    header: "Max Days to Harvest",
    cell: ({ row }) => h("div", String(row.getValue("max_days_to_harvest"))),
    enableSorting: true,
    enableFiltering: true,
  },
]

defineProps<{
  data: Crop[]
}>()
</script>

<template>
  <BaseDataTable
    :data="data"
    :columns="columns"
    :filterableColumns="['category', 'sunlight_requirement']"
    :searchableColumns="['name']"
  />
</template>
