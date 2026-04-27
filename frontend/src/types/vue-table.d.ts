import "@tanstack/vue-table"

declare module "@tanstack/vue-table" {
  interface TableMeta<TData> {
    update: (id: number, data: unknown) => void
    delete: (id: number) => void
    action?: (name: string, id: number) => void
  }
}

declare module "@tanstack/table-core" {
  interface TableMeta<TData> {
    update: (id: number, data: unknown) => void
    delete: (id: number) => void
    action?: (name: string, id: number) => void
  }
}
