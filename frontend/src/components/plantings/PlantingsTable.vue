<script setup lang="ts">
import { ref, computed, h } from "vue"
import {
  FlexRender,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  useVueTable,
  type ColumnDef,
  type SortingState,
  type ColumnFiltersState,
  type RowSelectionState,
} from "@tanstack/vue-table"
import type { Planting } from "@/types/planting"
import type { PaginationState } from "@/types/pagination"
import { columns as plantingColumns } from "./PlantingColumns"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Button } from "@/components/ui/button"
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"
import { IconGhost2, IconNotebook } from "@tabler/icons-vue"

const searchTerm = defineModel<string>("searchTerm", { default: "" })

const { data, rowCount, pagination } = defineProps<{
  data: Planting[]
  rowCount: number
  pagination: PaginationState
}>()

const emit = defineEmits<{
  (e: "pagination-change", value: PaginationState): void
  (e: "delete", value: number): void
  (e: "update", id: number, data: unknown): void
  (e: "action", name: string, id: number): void
  (e: "bulk-observe", plantingIds: number[]): void
}>()

const sorting = ref<SortingState>([])
const columnFilters = ref<ColumnFiltersState>([])
const rowSelection = ref<RowSelectionState>({})
const pageSizes = [5, 10, 20, 50]

const selectColumn: ColumnDef<Planting> = {
  id: "select",
  enableHiding: false,
  header: ({ table }) =>
    h(Checkbox, {
      modelValue: table.getIsAllPageRowsSelected(),
      "onUpdate:modelValue": (val: boolean | "indeterminate") =>
        table.toggleAllPageRowsSelected(val === true),
      "aria-label": "Select all",
    }),
  cell: ({ row }) =>
    h(Checkbox, {
      modelValue: row.getIsSelected(),
      "onUpdate:modelValue": (val: boolean | "indeterminate") => row.toggleSelected(val === true),
      "aria-label": "Select row",
    }),
}

const allColumns = [selectColumn, ...plantingColumns]

const table = useVueTable({
  manualPagination: true,
  manualFiltering: false,
  enableRowSelection: true,
  get data() {
    return data
  },
  get columns() {
    return allColumns
  },
  get rowCount() {
    return rowCount
  },
  meta: {
    delete: (id: number) => emit("delete", id),
    update: (id: number, val: unknown) => emit("update", id, val),
    action: (name: string, id: number) => emit("action", name, id),
  },
  getCoreRowModel: getCoreRowModel(),
  getSortedRowModel: getSortedRowModel(),
  getFilteredRowModel: getFilteredRowModel(),
  state: {
    get pagination() {
      return pagination
    },
    get globalFilter() {
      return searchTerm.value
    },
    get sorting() {
      return sorting.value
    },
    get columnFilters() {
      return columnFilters.value
    },
    get rowSelection() {
      return rowSelection.value
    },
  },
  onPaginationChange: (updaterOrValue) => {
    const nextState =
      typeof updaterOrValue === "function" ? updaterOrValue(pagination) : updaterOrValue
    emit("pagination-change", nextState)
  },
  onGlobalFilterChange: (updaterOrValue) => {
    searchTerm.value =
      typeof updaterOrValue === "function" ? updaterOrValue(searchTerm.value) : updaterOrValue
  },
  onSortingChange: (val) => {
    sorting.value = typeof val === "function" ? val(sorting.value) : val
  },
  onColumnFiltersChange: (val) => {
    columnFilters.value = typeof val === "function" ? val(columnFilters.value) : val
  },
  onRowSelectionChange: (val) => {
    rowSelection.value = typeof val === "function" ? val(rowSelection.value) : val
  },
})

const selectedCount = computed(() => table.getSelectedRowModel().rows.length)

const pages = computed(() => {
  const total = table.getPageCount()
  const current = table.getState().pagination.pageIndex + 1
  let start = Math.max(1, current - 2)
  let end = Math.min(total, start + 4)
  if (end - start < 4) {
    start = Math.max(1, end - 4)
  }
  const range = []
  for (let i = start; i <= end; i++) {
    range.push(i)
  }
  return range
})

const emitBulkObserve = (): void => {
  const ids = table.getSelectedRowModel().rows.map((row) => row.original.id)
  emit("bulk-observe", ids)
}
</script>

<template>
  <div class="w-full flex flex-col gap-4">
    <div class="flex flex-wrap items-center justify-between gap-2">
      <div class="flex items-center gap-2 w-full sm:w-auto">
        <div class="relative w-80 lg:w-96">
          <Input placeholder="Search..." v-model="searchTerm" class="pr-2 w-full" />
        </div>
      </div>
    </div>

    <!-- Bulk action toolbar -->
    <div v-if="selectedCount > 0" class="flex items-center gap-2">
      <span class="text-sm text-muted-foreground">{{ selectedCount }} selected</span>
      <Button size="sm" variant="outline" @click="emitBulkObserve">
        <IconNotebook :size="16" />
        Record Observation
      </Button>
    </div>

    <div class="overflow-hidden rounded-lg border">
      <Table>
        <TableHeader>
          <TableRow v-for="headerGroup in table.getHeaderGroups()" :key="headerGroup.id">
            <TableHead v-for="header in headerGroup.headers" :key="header.id">
              <FlexRender :render="header.column.columnDef.header" :props="header.getContext()" />
            </TableHead>
          </TableRow>
        </TableHeader>

        <TableBody>
          <template v-if="table.getRowModel().rows.length">
            <TableRow
              v-for="row in table.getRowModel().rows"
              :key="row.id"
              :data-state="row.getIsSelected() ? 'selected' : undefined"
            >
              <TableCell v-for="cell in row.getVisibleCells()" :key="cell.id">
                <FlexRender :render="cell.column.columnDef.cell" :props="cell.getContext()" />
              </TableCell>
            </TableRow>
          </template>
          <TableRow v-else>
            <TableCell :colspan="allColumns.length" class="h-32 text-center">
              <div class="flex flex-col items-center justify-center gap-2">
                <IconGhost2 class="w-8 h-8 text-muted-foreground" />
                <span class="text-muted-foreground">
                  {{ searchTerm ? "No results found." : "No data available." }}
                </span>
              </div>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </div>

    <div
      v-if="table.getRowModel().rows.length"
      class="flex flex-wrap items-center justify-between gap-4 py-4"
    >
      <div class="flex items-center gap-2">
        <Label class="text-sm font-medium">Rows per page</Label>
        <Select
          :model-value="`${table.getState().pagination.pageSize}`"
          @update:model-value="(val) => table.setPageSize(val as number)"
        >
          <SelectTrigger class="w-20">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem v-for="size in pageSizes" :key="size" :value="`${size}`">{{
              size
            }}</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div class="text-sm font-medium">
        Page {{ pagination.pageIndex + 1 }} of {{ table.getPageCount() }}
      </div>

      <div class="flex items-center gap-1">
        <Button
          size="sm"
          variant="outline"
          :disabled="!table.getCanPreviousPage()"
          @click="table.previousPage()"
        >
          Previous
        </Button>

        <div class="hidden sm:flex gap-1">
          <Button
            v-for="page in pages"
            :key="page"
            size="sm"
            variant="outline"
            :class="{
              'bg-primary text-primary-foreground hover:bg-primary':
                pagination.pageIndex === page - 1,
            }"
            @click="table.setPageIndex(page - 1)"
          >
            {{ page }}
          </Button>
        </div>

        <Button
          size="sm"
          variant="outline"
          :disabled="!table.getCanNextPage()"
          @click="table.nextPage()"
        >
          Next
        </Button>
      </div>
    </div>
  </div>
</template>
