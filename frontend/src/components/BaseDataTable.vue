<script setup lang="ts" generic="TData">
import { ref, computed, watch } from "vue"
import type {
  ColumnDef,
  SortingState,
  ColumnFiltersState,
  VisibilityState,
} from "@tanstack/vue-table"
import {
  FlexRender,
  getCoreRowModel,
  getPaginationRowModel,
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
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select"
import { Checkbox } from "@/components/ui/checkbox"
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
} from "@/components/ui/dropdown-menu"
import { Input } from "@/components/ui/input"

const props = defineProps<{
  data: TData[]
  columns: ColumnDef<TData>[]
  filterableColumns?: (keyof TData)[]
  searchableColumns?: (keyof TData)[] // optional, columns that are searchable
}>()

const sorting = ref<SortingState>([])
const columnFilters = ref<ColumnFiltersState>([])
const columnVisibility = ref<VisibilityState>({})
const rowSelection = ref({})
const pageSizes = [5, 10, 20, 50]

// --- Multi-column checklist filters state ---
const activeFilters = ref<Record<string, Set<string>>>({})

// --- Search state ---
const searchTerm = ref("")

function getUniqueValues(columnKey: keyof TData) {
  return Array.from(new Set(props.data.map((item) => String(item[columnKey]))))
}

function toggleFilter(column: keyof TData, value: string) {
  if (!activeFilters.value[column]) activeFilters.value[column] = new Set()
  if (activeFilters.value[column].has(value)) activeFilters.value[column].delete(value)
  else activeFilters.value[column].add(value)
}

// Computed filtered data based on checklist selections + search
const filteredData = computed(() => {
  let data = props.data

  // Apply checklist filters
  if (props.filterableColumns && Object.keys(activeFilters.value).length > 0) {
    data = data.filter((item) =>
      Object.entries(activeFilters.value).every(([col, values]) => {
        if (!values.size) return true
        return values.has(String(item[col as keyof TData]))
      }),
    )
  }

  // Apply search
  if (searchTerm.value.trim()) {
    const term = searchTerm.value.toLowerCase()
    const colsToSearch = props.searchableColumns?.length
      ? props.searchableColumns
      : (props.columns.map((c) => c.accessorKey).filter(Boolean) as (keyof TData)[])
    data = data.filter((item) =>
      colsToSearch.some((col) =>
        String(item[col] ?? "")
          .toLowerCase()
          .includes(term),
      ),
    )
  }

  return data
})

const table = useVueTable({
  get data() {
    return filteredData.value
  },
  get columns() {
    return props.columns
  },
  getCoreRowModel: getCoreRowModel(),
  getPaginationRowModel: getPaginationRowModel(),
  getSortedRowModel: getSortedRowModel(),
  getFilteredRowModel: getFilteredRowModel(),
  state: {
    get sorting() {
      return sorting.value
    },
    get columnFilters() {
      return columnFilters.value
    },
    get columnVisibility() {
      return columnVisibility.value
    },
    get rowSelection() {
      return rowSelection.value
    },
  },
  onSortingChange: (val) => {
    sorting.value = typeof val === "function" ? val(sorting.value) : val
  },
  onColumnFiltersChange: (val) => {
    columnFilters.value = typeof val === "function" ? val(columnFilters.value) : val
  },
  onColumnVisibilityChange: (val) => {
    columnVisibility.value = typeof val === "function" ? val(columnVisibility.value) : val
  },
  onRowSelectionChange: (val) => {
    rowSelection.value = typeof val === "function" ? val(rowSelection.value) : val
  },
})

// Pagination pages
const pages = computed(() => Array.from({ length: table.getPageCount() }, (_, i) => i + 1))
</script>

<template>
  <div class="w-full flex flex-col gap-4">
    <!-- Global / column search -->
    <div class="flex flex-wrap gap-2 items-center">
      <Input placeholder="Search..." v-model="searchTerm" class="max-w-sm" />
    </div>

    <!-- Multi-column checklist filters -->
    <div v-if="filterableColumns?.length" class="flex flex-wrap gap-2">
      <div v-for="col in filterableColumns" :key="col">
        <DropdownMenu>
          <DropdownMenuTrigger as-child>
            <Button size="sm" variant="outline">{{ String(col) }}</Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent>
            <DropdownMenuItem
              v-for="value in getUniqueValues(col)"
              :key="value"
              class="flex items-center gap-2"
            >
              <Checkbox
                :model-value="activeFilters[col]?.has(value) || false"
                @update:model-value="() => toggleFilter(col, value)"
              />
              <span>{{ value }}</span>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </div>

    <!-- Table -->
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
                <span v-if="header.column.getIsSorted() === 'asc'">⬆️</span>
                <span v-else-if="header.column.getIsSorted() === 'desc'">⬇️</span>
              </Button>
              <div v-else>
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
            <TableCell :col-span="props.columns.length" class="text-center h-24">
              No results.
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </div>

    <!-- Pagination -->
    <div class="flex flex-wrap items-center justify-between gap-2 py-4">
      <div class="flex items-center gap-2">
        <span class="text-sm text-muted-foreground">Rows per page:</span>
        <Select
          v-model="table.getState().pagination.pageSize"
          @update:model-value="(val) => table.setPageSize(Number(val))"
        >
          <SelectTrigger class="w-20">
            <SelectValue :placeholder="`${table.getState().pagination.pageSize}`" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem v-for="size in pageSizes" :key="size" :value="size">{{ size }}</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div class="text-sm text-muted-foreground">
        {{ table.getState().pagination.pageIndex + 1 }} of {{ table.getPageCount() }} pages
      </div>

      <div class="flex gap-1">
        <Button
          size="sm"
          variant="outline"
          :disabled="!table.getCanPreviousPage()"
          @click="table.previousPage()"
          >Previous</Button
        >
        <Button
          v-for="page in pages"
          :key="page"
          size="sm"
          variant="outline"
          :class="{ 'bg-primary text-white': table.getState().pagination.pageIndex === page - 1 }"
          @click="table.setPageIndex(page - 1)"
        >
          {{ page }}
        </Button>
        <Button
          size="sm"
          variant="outline"
          :disabled="!table.getCanNextPage()"
          @click="table.nextPage()"
          >Next</Button
        >
      </div>
    </div>
  </div>
</template>
