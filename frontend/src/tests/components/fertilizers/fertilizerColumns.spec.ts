import { describe, it, expect, vi } from "vitest"
import { defineComponent } from "vue"
import { mount } from "@vue/test-utils"
import { columns } from "@/components/fertilizers/FertilizerColumns"
import FertilizerTableActions from "@/components/fertilizers/FertilizerTableActions.vue"
import type { Fertilizer } from "@/types/fertilizer"

const mockFertilizer: Fertilizer = {
  id: 1,
  name: "Swamp Fertilizer #1",
  type: "SWAMP",
  status: "BREWING",
  startDate: "2024-01-01",
  ingredients: ["banana peels", "molasses"],
  notes: "",
  createdAt: "2024-01-01T00:00:00Z",
  updatedAt: "2024-01-01T00:00:00Z",
}

const mockRow = {
  getValue: (key: string) => mockFertilizer[key as keyof Fertilizer],
  original: mockFertilizer,
}

const mockTable = {
  options: { meta: { update: vi.fn(), delete: vi.fn(), action: vi.fn() } },
}

function getVnode(colId: string) {
  const col = columns.find((c) => c.id === colId)!

  type CellFn = (ctx: { row: typeof mockRow; table: typeof mockTable }) => unknown
  return (col as unknown as { cell: CellFn }).cell({ row: mockRow, table: mockTable })
}

function renderCell(colId: string) {
  const vnode = getVnode(colId)
  return mount(defineComponent({ render: () => vnode }))
}

describe("FertilizerColumns", () => {
  it("name column renders fertilizer name", () => {
    expect(renderCell("name").text()).toBe("Swamp Fertilizer #1")
  })

  it("type column renders the type label", () => {
    expect(renderCell("type").text()).toBe("Swamp")
  })

  it("status column renders the status label", () => {
    expect(renderCell("status").text()).toBe("Brewing")
  })

  it("ingredients column renders a dash when there are no ingredients", () => {
    const emptyRow = {
      getValue: (key: string) =>
        key === "ingredients" ? [] : mockFertilizer[key as keyof Fertilizer],
      original: mockFertilizer,
    }
    const col = columns.find((c) => c.id === "ingredients")!
    type CellFn = (ctx: { row: typeof emptyRow }) => unknown
    const vnode = (col as unknown as { cell: CellFn }).cell({ row: emptyRow })
    expect(mount(defineComponent({ render: () => vnode })).text()).toBe("—")
  })

  it("ingredients column returns one badge vnode per ingredient", () => {
    const vnode = getVnode("ingredients")
    expect(Array.isArray(vnode.children)).toBe(true)
    expect((vnode.children as unknown[]).length).toBe(2)
  })

  it("actions column cell type is FertilizerTableActions", () => {
    expect(getVnode("actions").type).toBe(FertilizerTableActions)
  })
})
