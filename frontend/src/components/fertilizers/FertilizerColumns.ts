import type { ColumnDef } from "@tanstack/vue-table"
import { h } from "vue"
import type { Fertilizer, FertilizerStatus, FertilizerType } from "@/types/fertilizer"
import FertilizerTableActions from "./FertilizerTableActions.vue"
import { Badge } from "@/components/ui/badge"
import { formatDate } from "@/utils/formatting"

const TYPE_BADGE_VARIANT: Record<FertilizerType, "secondary" | "outline" | "default"> = {
  SWAMP: "default",
  COMPOST: "secondary",
  OTHER: "outline",
}

const STATUS_BADGE_VARIANT: Record<
  FertilizerStatus,
  "default" | "secondary" | "destructive" | "outline"
> = {
  BREWING: "default",
  READY: "secondary",
  USED: "outline",
  DISCARDED: "destructive",
}

const TYPE_LABEL: Record<FertilizerType, string> = {
  SWAMP: "Swamp",
  COMPOST: "Compost",
  OTHER: "Other",
}

const STATUS_LABEL: Record<FertilizerStatus, string> = {
  BREWING: "Brewing",
  READY: "Ready",
  USED: "Used",
  DISCARDED: "Discarded",
}

export const columns: ColumnDef<Fertilizer>[] = [
  {
    id: "name",
    accessorKey: "name",
    header: "Name",
    cell: ({ row }) => h("div", row.getValue("name")),
    enableSorting: true,
  },
  {
    id: "type",
    accessorKey: "type",
    header: "Type",
    cell: ({ row }) => {
      const type = row.getValue<string>("type") as FertilizerType
      return h(
        Badge,
        { variant: TYPE_BADGE_VARIANT[type] ?? "outline" },
        () => TYPE_LABEL[type] ?? type,
      )
    },
    enableSorting: false,
  },
  {
    id: "status",
    accessorKey: "status",
    header: "Status",
    cell: ({ row }) => {
      const status = row.getValue<string>("status") as FertilizerStatus
      return h(
        Badge,
        { variant: STATUS_BADGE_VARIANT[status] ?? "outline" },
        () => STATUS_LABEL[status] ?? status,
      )
    },
    enableSorting: false,
  },
  {
    id: "startDate",
    accessorKey: "startDate",
    header: "Started On",
    cell: ({ row }) => h("div", formatDate(row.getValue("startDate"))),
    enableSorting: true,
  },
  {
    id: "ingredients",
    accessorKey: "ingredients",
    header: "Ingredients",
    cell: ({ row }) => {
      const values = row.getValue<string[]>("ingredients") ?? []
      if (!values.length) return h("div", "—")
      return h(
        "div",
        { class: "flex flex-wrap gap-1" },
        values.map((v) => h(Badge, { variant: "secondary" }, () => v)),
      )
    },
    enableSorting: false,
  },
  {
    id: "actions",
    enableHiding: false,
    cell: ({ row, table }) => h(FertilizerTableActions, { row, table }),
  },
]
