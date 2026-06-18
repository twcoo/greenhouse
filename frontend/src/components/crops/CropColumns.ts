import type { ColumnDef } from "@tanstack/vue-table"
import { h } from "vue"
import type { Crop } from "@/types/crop"
import CropTableActions from "./CropTableActions.vue"
import { includesMultiple } from "@/utils/filterFns"

export const columns: ColumnDef<Crop>[] = [
  {
    id: "name",
    accessorKey: "name",
    header: "Name",
    cell: ({ row }) => h("div", row.getValue("name")),
    enableSorting: true,
  },
  {
    id: "scientificName",
    accessorKey: "scientificName",
    header: "Scientific Name",
    cell: ({ row }) => h("div", row.getValue("scientificName")),
    enableSorting: true,
  },
  {
    id: "category",
    accessorKey: "category",
    header: "Category",
    cell: ({ row }) => h("div", row.getValue("category")),
    enableSorting: true,
    filterFn: includesMultiple,
  },
  {
    id: "sunlightRequirement",
    accessorKey: "sunlightRequirement",
    header: "Sunlight",
    cell: ({ row }) => h("div", row.getValue("sunlightRequirement")),
    enableSorting: true,
    filterFn: includesMultiple,
  },
  {
    id: "minDaysToHarvest",
    accessorKey: "minDaysToHarvest",
    header: "Min Days to Harvest",
    cell: ({ row }) => h("div", String(row.getValue("minDaysToHarvest"))),
    enableSorting: true,
  },
  {
    id: "maxDaysToHarvest",
    accessorKey: "maxDaysToHarvest",
    header: "Max Days to Harvest",
    cell: ({ row }) => h("div", String(row.getValue("maxDaysToHarvest"))),
    enableSorting: true,
  },
  {
    id: "actions",
    enableHiding: false,
    cell: ({ row, table }) => h(CropTableActions, { row, table }),
  },
]
