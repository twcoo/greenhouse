import type { ColumnDef } from "@tanstack/vue-table"
import { h } from "vue"
import type { Planting } from "@/types/planting"
import PlantingTableActions from "./PlantingTableActions.vue"

const formatDate = (value: string): string =>
  new Intl.DateTimeFormat("en-US", { dateStyle: "medium" }).format(new Date(value))

export const columns: ColumnDef<Planting>[] = [
  {
    id: "cropName",
    accessorKey: "cropName",
    header: "Crop",
    cell: ({ row }) => h("div", row.getValue("cropName")),
    enableSorting: true,
  },
  {
    id: "varietyName",
    accessorKey: "varietyName",
    header: "Variety",
    cell: ({ row }) => h("div", row.getValue("varietyName")),
    enableSorting: true,
  },
  {
    id: "createdAt",
    accessorKey: "createdAt",
    header: "Planted On",
    cell: ({ row }) => h("div", formatDate(row.getValue("createdAt"))),
    enableSorting: true,
  },
  {
    id: "actions",
    enableHiding: false,
    cell: ({ row, table }) => h(PlantingTableActions, { row, table }),
  },
]
