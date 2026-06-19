import type { FilterFn, Row } from "@tanstack/vue-table"

 
export const includesMultiple: FilterFn<any> = (
  row: Row<unknown>,
  columnId: string,
  filterValue: unknown,
) => {
  if (!Array.isArray(filterValue) || filterValue.length === 0) {
    return true
  }

  const cellValue = row.getValue(columnId)
  const searchableValue = cellValue !== null && cellValue !== undefined ? String(cellValue) : ""

  return (filterValue as unknown[]).some((val) => String(val) === searchableValue)
}
