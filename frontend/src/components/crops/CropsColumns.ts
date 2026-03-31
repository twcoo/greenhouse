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
    accessorKey: "scientific_name",
    header: "Scientific Name",
    cell: ({ row }) => h("div", row.getValue("scientific_name")),
    enableSorting: true,
  },
  {
    accessorKey: "category",
    header: "Category",
    cell: ({ row }) => h("div", row.getValue("category")),
    enableSorting: true,
  },
  {
    accessorKey: "sunlight_requirement",
    header: "Sunlight",
    cell: ({ row }) => h("div", row.getValue("sunlight_requirement")),
    enableSorting: true,
  },
  {
    accessorKey: "min_days_to_harvest",
    header: "Min Days to Harvest",
    cell: ({ row }) => h("div", String(row.getValue("min_days_to_harvest"))),
    enableSorting: true,
  },
  {
    accessorKey: "max_days_to_harvest",
    header: "Max Days to Harvest",
    cell: ({ row }) => h("div", String(row.getValue("max_days_to_harvest"))),
    enableSorting: true,
  },
]
