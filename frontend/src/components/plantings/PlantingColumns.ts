import type { ColumnDef } from "@tanstack/vue-table"
import { h } from "vue"
import type { Planting } from "@/types/planting"
import PlantingTableActions from "./PlantingTableActions.vue"
import { formatDate } from "@/utils/formatting"

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
    id: "currentLocation",
    accessorKey: "currentLocation",
    header: "Location",
    cell: ({ row }) => h("div", row.getValue("currentLocation") ?? "—"),
    enableSorting: false,
  },
  {
    id: "actions",
    enableHiding: false,
    cell: ({ row, table }) => h(PlantingTableActions, { row, table }),
  },
]
