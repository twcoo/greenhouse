import { describe, it, expect, vi } from "vitest"
import { defineComponent } from "vue"
import { mount } from "@vue/test-utils"
import { columns } from "@/components/plantings/PlantingColumns"
import PlantingTableActions from "@/components/plantings/PlantingTableActions.vue"
import type { Planting } from "@/types/planting"

const mockPlanting: Planting = {
  id: 1,
  crop: 1,
  cropName: "Tomato",
  variety: 1,
  varietyName: "Sun Gold",
  currentLocation: "Greenhouse A",
  // Use a midday UTC date to avoid timezone edge cases in formatted output
  createdAt: "2024-06-15T12:00:00Z",
}

const mockRow = {
  getValue: (key: string) => mockPlanting[key as keyof Planting],
  original: mockPlanting,
}

const mockTable = {
  options: { meta: { update: vi.fn(), delete: vi.fn() } },
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

describe("PlantingColumns", () => {
  it("cropName column renders the crop name", () => {
    expect(renderCell("cropName").text()).toBe("Tomato")
  })

  it("varietyName column renders the variety name", () => {
    expect(renderCell("varietyName").text()).toBe("Sun Gold")
  })

  it("createdAt column renders a formatted date string containing the year", () => {
    const text = renderCell("createdAt").text()
    expect(text).toContain("2024")
    expect(text).not.toBe(mockPlanting.createdAt)
  })

  it("currentLocation column renders the location name", () => {
    expect(renderCell("currentLocation").text()).toBe("Greenhouse A")
  })

  it("currentLocation column renders dash when null", () => {
    const original = mockPlanting.currentLocation
    mockPlanting.currentLocation = null
    expect(renderCell("currentLocation").text()).toBe("—")
    mockPlanting.currentLocation = original
  })

  it("actions column cell type is PlantingTableActions", () => {
    expect(getVnode("actions").type).toBe(PlantingTableActions)
  })
})
