import type { ColumnDef } from "@tanstack/vue-table"
import { h } from "vue"
import type { Planting } from "@/types/planting"
import PlantingTableActions from "./PlantingTableActions.vue"
import { Badge } from "@/components/ui/badge"
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
    id: "status",
    accessorKey: "status",
    header: "Status",
    cell: ({ row }) => {
      const status = row.getValue<string>("status")
      const variantMap: Record<string, "default" | "secondary" | "destructive" | "outline"> = {
        ACTIVE: "default",
        HARVESTED: "secondary",
        DEAD: "destructive",
        REMOVED: "outline",
      }
      const labelMap: Record<string, string> = {
        ACTIVE: "Active",
        HARVESTED: "Harvested",
        DEAD: "Dead",
        REMOVED: "Removed",
      }
      return h(
        Badge,
        { variant: variantMap[status] ?? "outline" },
        () => labelMap[status] ?? status,
      )
    },
    enableSorting: false,
  },
  {
    id: "hasDailyObservation",
    accessorKey: "hasDailyObservation",
    header: "Today's Observation",
    cell: ({ row }) => {
      const has = row.getValue<boolean>("hasDailyObservation")
      return has
        ? h(Badge, { variant: "default" }, () => "Recorded")
        : h(Badge, { variant: "outline" }, () => "Pending")
    },
    enableSorting: false,
  },
  {
    id: "actions",
    enableHiding: false,
    cell: ({ row, table }) => h(PlantingTableActions, { row, table }),
  },
]
