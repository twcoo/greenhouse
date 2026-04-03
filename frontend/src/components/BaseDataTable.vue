<script setup lang="ts" generic="TData">
import { ref, computed, watch } from "vue"
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
import { IconSortAscending, IconSortDescending, IconGhost2 } from "@tabler/icons-vue"
import { Ref } from "vue"

const props = defineProps<{
  data: TData[]
  columns: ColumnDef<TData>[]
  filterableColumns?: (keyof TData)[]
  rowCount: number
  pagination: Ref<PaginationState>
}>()

const emit = defineEmits<{
  (e: "pagination-change", value: PaginationState): void
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
  rowCount: 12,
  get data() {
    return props.data
  },
  get columns() {
    return props.columns
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
  const total = table.getPageCount()
  const current = table.getState().pagination.pageIndex + 1

  // Logic to show a limited range, e.g., 5 pages centered around current
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

console.log(props.rowCount)
console.log(table.getCanPreviousPage())
console.log(table.getCanNextPage())
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
              <Button
                v-if="header.column.getCanSort()"
                variant="ghost"
                size="sm"
                class="flex items-center gap-1"
                @click="header.column.toggleSorting(header.column.getIsSorted() === 'asc')"
              >
                <FlexRender :render="header.column.columnDef.header" :props="header.getContext()" />
                <span v-if="header.column.getIsSorted() === 'asc'">
                  <IconSortAscending :size="16" />
                </span>
                <span v-else-if="header.column.getIsSorted() === 'desc'">
                  <IconSortDescending :size="16" />
                </span>
              </Button>
              <div v-else class="px-3 py-2">
                <FlexRender :render="header.column.columnDef.header" :props="header.getContext()" />
              </div>
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
            <TableCell :col-span="columns.length" class="h-32 text-center">
              <div class="flex flex-col items-center justify-center gap-2">
                <IconGhost2 class="w-8 h-8 text-muted-foreground" />
                <span class="text-muted-foreground">No results found.</span>
              </div>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </div>

    <div class="flex flex-wrap items-center justify-between gap-4 py-4">
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
