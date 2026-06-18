import { describe, it, expect, vi } from "vitest"
import { defineComponent } from "vue"
import { mount } from "@vue/test-utils"
import { columns } from "@/components/planting-locations/PlantingLocationColumns"
import PlantingLocationTableActions from "@/components/planting-locations/PlantingLocationTableActions.vue"
import type { PlantingLocation } from "@/types/plantingLocation"
import { includesMultiple } from "@/utils/filterFns"

const mockLocation: PlantingLocation = {
  id: 1,
  name: "Garden Pot",
  locationType: "POT",
  width: 30,
  height: 40,
  currentStatus: null,
}

const mockLocationNoOptionals: PlantingLocation = {
  id: 2,
  name: "Garden Bed",
  locationType: "GROUND",
  width: 100,
  currentStatus: null,
}

const mockTable = {
  options: { meta: { update: vi.fn(), delete: vi.fn() } },
}

function getVnode(colId: string, location: PlantingLocation = mockLocation) {
  const col = columns.find((c) => c.id === colId)!
  const mockRow = {
    getValue: (key: string) => location[key as keyof PlantingLocation],
    original: location,
  }

  type CellFn = (ctx: { row: typeof mockRow; table: typeof mockTable }) => unknown
  return (col as unknown as { cell: CellFn }).cell({ row: mockRow, table: mockTable })
}

function renderCell(colId: string, location: PlantingLocation = mockLocation) {
  return mount(defineComponent({ render: () => getVnode(colId, location) }))
}

describe("PlantingLocationColumns", () => {
  it("name column renders location name", () => {
    expect(renderCell("name").text()).toBe("Garden Pot")
  })

  it("width column renders width as string", () => {
    expect(renderCell("width").text()).toBe("30")
  })

  it("height column renders height when present", () => {
    expect(renderCell("height").text()).toBe("40")
  })

  it("height column renders dash when height is absent", () => {
    expect(renderCell("height", mockLocationNoOptionals).text()).toBe("-")
  })

  it("length column renders dash when length is absent", () => {
    expect(renderCell("length", mockLocation).text()).toBe("-")
  })

  it("currentStatus column renders dash when currentStatus is null", () => {
    expect(renderCell("currentStatus", mockLocation).text()).toBe("-")
  })

  it("currentStatus column renders Available label for AVAILABLE status", () => {
    const location: PlantingLocation = {
      ...mockLocation,
      currentStatus: { id: 1, status: "AVAILABLE", notes: "", createdAt: "2024-01-01T00:00:00Z" },
    }
    expect(renderCell("currentStatus", location).text()).toBe("Available")
  })

  it("currentStatus column renders In Use label for IN_USE status", () => {
    const location: PlantingLocation = {
      ...mockLocation,
      currentStatus: { id: 2, status: "IN_USE", notes: "", createdAt: "2024-01-01T00:00:00Z" },
    }
    expect(renderCell("currentStatus", location).text()).toBe("In Use")
  })

  it("currentStatus column renders Damaged label for DAMAGED status", () => {
    const location: PlantingLocation = {
      ...mockLocation,
      currentStatus: { id: 3, status: "DAMAGED", notes: "", createdAt: "2024-01-01T00:00:00Z" },
    }
    expect(renderCell("currentStatus", location).text()).toBe("Damaged")
  })

  it("currentStatus column renders Destroyed label for DESTROYED status", () => {
    const location: PlantingLocation = {
      ...mockLocation,
      currentStatus: { id: 4, status: "DESTROYED", notes: "", createdAt: "2024-01-01T00:00:00Z" },
    }
    expect(renderCell("currentStatus", location).text()).toBe("Destroyed")
  })

  it("actions column cell type is PlantingLocationTableActions", () => {
    expect(getVnode("actions").type).toBe(PlantingLocationTableActions)
  })

  it("locationType column uses includesMultiple filterFn for exact matching", () => {
    const col = columns.find((c) => c.id === "locationType")!
    expect((col as { filterFn?: unknown }).filterFn).toBe(includesMultiple)
  })
})
