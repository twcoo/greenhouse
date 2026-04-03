import type { ColumnDef } from "@tanstack/vue-table"
import { h } from "vue"
import type { Crop } from "@/types/crop"

export const columns: ColumnDef<Crop>[] = [
  {
    accessorKey: "name",
    header: "Name",
    cell: ({ row }) => h("div", row.getValue("name")),
    enableSorting: true,
  },
  {
    accessorKey: "scientificName",
    header: "Scientific Name",
    cell: ({ row }) => h("div", row.getValue("scientificName")),
    enableSorting: true,
  },
  {
    accessorKey: "category",
    header: "Category",
    cell: ({ row }) => h("div", row.getValue("category")),
    enableSorting: true,
  },
  {
    accessorKey: "sunlightRequirement",
    header: "Sunlight",
    cell: ({ row }) => h("div", row.getValue("sunlightRequirement")),
    enableSorting: true,
  },
  {
    accessorKey: "minDaysToHarvest",
    header: "Min Days to Harvest",
    cell: ({ row }) => h("div", String(row.getValue("minDaysToHarvest"))),
    enableSorting: true,
  },
  {
    accessorKey: "maxDaysToHarvest",
    header: "Max Days to Harvest",
    cell: ({ row }) => h("div", String(row.getValue("maxDaysToHarvest"))),
    enableSorting: true,
  },
]
