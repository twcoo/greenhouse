<script setup lang="ts" generic="TData">
import { ref, computed } from "vue"
import { ColumnDef, SortingState, ColumnFiltersState, PaginationState } from "@tanstack/vue-table"
import {
  FlexRender,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  useVueTable,
} from "@tanstack/vue-table"
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
  SelectGroup,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { toTitleCase } from "@/utils/formatting"
import { Ref } from "vue"
import { IconGhost2 } from "@tabler/icons-vue"

const props = defineProps<{
  data: TData[]
  columns: ColumnDef<TData>[]
  filterableColumns?: (keyof TData)[]
  rowCount: number
  pagination: Ref<PaginationState>
}>()

const emit = defineEmits<{
  (e: "pagination-change", value: PaginationState): void
  (e: "delete", value: number): void
  (e: "update", id: number, data: any): void
}>()

const sorting = ref<SortingState>([])
const columnFilters = ref<ColumnFiltersState>([])
const pageSizes = [5, 10, 20, 50]
const searchTerm = ref("")

const filterFns = {
  includesMultiple: (row, columnId, filterValue) => {
    if (!filterValue?.length) return true
    return filterValue.includes(String(row.getValue(columnId)))
  },
}

const filterOptionsMap = computed(() => {
  const map: Record<string, Set<unknown>> = {}
  if (!props.filterableColumns) return map
  for (const col of props.filterableColumns) {
    map[col as string] = new Set()
  }
  for (const item of props.data) {
    for (const col of props.filterableColumns) {
      map[col as string].add(item[col])
    }
  }
  return map
})

function getFilterOptions(columnKey: keyof TData) {
  return [...(filterOptionsMap.value[columnKey as string] ?? [])]
}

const table = useVueTable({
  manualPagination: true,
  rowCount: props.rowCount,
  get data() {
    return props.data
  },
  get columns() {
    return props.columns
  },
  meta: {
    delete: (id: number) => emit("delete", id),
    update: (id: number, data: any) => emit("update", id, data),
  },
  filterFns,
  getCoreRowModel: getCoreRowModel(),
  getSortedRowModel: getSortedRowModel(),
  getFilteredRowModel: getFilteredRowModel(),
  state: {
    get pagination() {
      return props.pagination
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
  },
  onPaginationChange: (updaterOrValue) => {
    const nextState =
      typeof updaterOrValue === "function" ? updaterOrValue(props.pagination) : updaterOrValue
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
})

const pages = computed(() => {
  // 1. Get the total count of pages available (e.g., 20)
  const total = table.getPageCount()

  // 2. Get the current page index.
  // We add 1 because TanStack is 0-indexed (Index 0 = Page 1)
  const current = table.getState().pagination.pageIndex + 1

  // 3. Define the starting point of our window.
  // We want the current page to be in the middle, so we subtract 2.
  // Math.max(1, ...) ensures we never go below Page 1 (prevents 0 or negative numbers).
  let start = Math.max(1, current - 2)

  // 4. Define the end point of our window.
  // We want to show a spread of 5 buttons total, so we add 4 to the 'start'.
  // Math.min(total, ...) ensures we never go past the last page.
  let end = Math.min(total, start + 4)

  // 5. The "Left-Side" Correction:
  // If we are near the end (e.g., Page 20 of 20), the 'end' is capped.
  // This check ensures that if we have fewer than 5 buttons visible,
  // we push the 'start' back to fill the gap so we always show 5 buttons if possible.
  if (end - start < 4) {
    start = Math.max(1, end - 4)
  }

  // 6. Generate the actual array of numbers.
  // If start is 8 and end is 12, this creates: [8, 9, 10, 11, 12]
  const range = []
  for (let i = start; i <= end; i++) {
    range.push(i)
  }

  return range
})
</script>

<template>
  <div class="w-full flex flex-col gap-4">
    <div class="flex flex-wrap items-center justify-between gap-2">
      <div class="flex items-center gap-2 w-full sm:w-auto">
        <div class="relative w-80 lg:w-96">
          <Input placeholder="Search..." v-model="searchTerm" class="pr-2 w-full" />
        </div>
      </div>

      <div v-if="filterableColumns?.length" class="flex flex-wrap gap-2 items-center">
        <Label class="text-sm font-medium"> Filter By: </Label>
        <div v-for="col in filterableColumns" :key="col">
          <Select
            :model-value="table.getColumn(col as string)?.getFilterValue() ?? ''"
            @update:model-value="
              (value) => table.getColumn(col as string)?.setFilterValue(value || undefined)
            "
          >
            <SelectTrigger class="w-[200px]">
              <SelectValue :placeholder="`${toTitleCase(col as string)}`" />
              <SelectContent>
                <SelectGroup>
                  <SelectItem :value="null">All</SelectItem>
                  <SelectItem v-for="value in getFilterOptions(col)" :key="value" :value="value">
                    {{ value }}
                  </SelectItem>
                </SelectGroup>
              </SelectContent>
            </SelectTrigger>
          </Select>
        </div>
      </div>
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
            <TableRow v-for="row in table.getRowModel().rows" :key="row.id">
              <TableCell v-for="cell in row.getVisibleCells()" :key="cell.id">
                <FlexRender :render="cell.column.columnDef.cell" :props="cell.getContext()" />
              </TableCell>
            </TableRow>
          </template>
          <TableRow v-else>
            <TableCell :colspan="columns.length" class="h-32 text-center">
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
          @update:model-value="(val) => table.setPageSize(val)"
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
