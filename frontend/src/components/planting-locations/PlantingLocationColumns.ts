import type { ColumnDef } from "@tanstack/vue-table"
import { h } from "vue"
import type { PlantingLocation } from "@/types/plantingLocation"
import { Badge } from "@/components/ui/badge"
import PlantingLocationTableActions from "./PlantingLocationTableActions.vue"

export const columns: ColumnDef<PlantingLocation>[] = [
  {
    id: "name",
    accessorKey: "name",
    header: "Name",
    cell: ({ row }) => h("div", row.getValue("name")),
    enableSorting: true,
  },
  {
    id: "locationType",
    accessorKey: "locationType",
    header: "Type",
    cell: ({ row }) => h("div", row.getValue("locationType")),
    enableSorting: true,
  },
  {
    id: "width",
    accessorKey: "width",
    header: "Width (cm)",
    cell: ({ row }) => h("div", String(row.getValue("width"))),
    enableSorting: true,
  },
  {
    id: "height",
    accessorKey: "height",
    header: "Height (cm)",
    cell: ({ row }) => {
      const height = row.getValue("height")
      return h("div", height ? String(height) : "-")
    },
    enableSorting: true,
  },
  {
    id: "length",
    accessorKey: "length",
    header: "Length (m)",
    cell: ({ row }) => {
      const length = row.getValue("length")
      return h("div", length ? String(length) : "-")
    },
    enableSorting: true,
  },
  {
    id: "isOccupied",
    accessorKey: "isOccupied",
    header: "Status",
    cell: ({ row }) => {
      const location = row.original
      const isPot =
        location.locationType === "NURSERYPOT" || location.locationType === "POT"

      if (!isPot) return h("div", "-")

      return h(
        Badge,
        { variant: location.isOccupied ? "destructive" : "secondary" },
        () => (location.isOccupied ? "Occupied" : "Available"),
      )
    },
    enableSorting: false,
  },
  {
    id: "actions",
    enableHiding: false,
    cell: ({ row, table }) => h(PlantingLocationTableActions, { row, table }),
  },
]
