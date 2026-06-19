import type { ColumnDef } from "@tanstack/vue-table"
import { h } from "vue"
import type { PlantingLocation } from "@/types/plantingLocation"
import type { PlantingLocationStatusChoice } from "@/types/plantingLocationStatus"
import { Badge } from "@/components/ui/badge"
import PlantingLocationTableActions from "./PlantingLocationTableActions.vue"
import { includesMultiple } from "@/utils/filterFns"

const STATUS_BADGE_VARIANT: Record<
  PlantingLocationStatusChoice,
  "secondary" | "default" | "destructive" | "outline"
> = {
  AVAILABLE: "secondary",
  IN_USE: "default",
  DAMAGED: "outline",
  DESTROYED: "destructive",
  RETIRED: "destructive",
}

const STATUS_LABEL: Record<PlantingLocationStatusChoice, string> = {
  AVAILABLE: "Available",
  IN_USE: "In Use",
  DAMAGED: "Damaged",
  DESTROYED: "Destroyed",
  RETIRED: "Retired",
}

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
    filterFn: includesMultiple,
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
    id: "currentStatus",
    accessorKey: "currentStatus",
    header: "Condition",
    cell: ({ row }) => {
      const current = row.original.currentStatus
      if (!current) return h("div", "-")

      const choice = current.status as PlantingLocationStatusChoice
      return h(Badge, { variant: STATUS_BADGE_VARIANT[choice] }, () => STATUS_LABEL[choice])
    },
    enableSorting: false,
  },
  {
    id: "actions",
    enableHiding: false,
    cell: ({ row, table }) => h(PlantingLocationTableActions, { row, table }),
  },
]
