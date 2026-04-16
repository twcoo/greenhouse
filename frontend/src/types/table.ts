import type { Table } from "@tanstack/vue-table"

export interface TableRowProps<T> {
  row: {
    original: T
  }
  table: Table<T>
}
