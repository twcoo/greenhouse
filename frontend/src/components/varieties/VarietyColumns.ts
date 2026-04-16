import type { ColumnDef } from "@tanstack/vue-table"
import { h } from "vue"
import type { Variety } from "@/types/variety"
import VarietyTableActions from "./VarietyTableActions.vue"
import { Badge } from "@/components/ui/badge"

export const columns: ColumnDef<Variety>[] = [
  {
    id: "name",
    accessorKey: "name",
    header: "Name",
    cell: ({ row }) => h("div", row.getValue("name")),
    enableSorting: true,
  },
  {
    id: "cropName",
    accessorKey: "cropName",
    header: "Crop",
    cell: ({ row }) => h("div", row.getValue("cropName")),
    enableSorting: true,
  },
  {
    id: "growthHabit",
    accessorKey: "growthHabit",
    header: "Growth Habit",
    cell: ({ row }) => {
      const values = row.getValue<string[]>("growthHabit")
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
    cell: ({ row, table }) => h(VarietyTableActions, { row, table }),
  },
]
