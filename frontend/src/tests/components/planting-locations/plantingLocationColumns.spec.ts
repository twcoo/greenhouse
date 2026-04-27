import { describe, it, expect, vi } from "vitest"
import { defineComponent } from "vue"
import { mount } from "@vue/test-utils"
import { columns } from "@/components/planting-locations/PlantingLocationColumns"
import PlantingLocationTableActions from "@/components/planting-locations/PlantingLocationTableActions.vue"
import type { PlantingLocation } from "@/types/plantingLocation"

const mockLocation: PlantingLocation = {
  id: 1,
  name: "Garden Pot",
  locationType: "POT",
  width: 30,
  height: 40,
  isOccupied: false,
}

const mockLocationNoOptionals: PlantingLocation = {
  id: 2,
  name: "Garden Bed",
  locationType: "GROUND",
  width: 100,
  isOccupied: false,
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

  it("isOccupied column renders Available badge for an unoccupied pot", () => {
    const availablePot: PlantingLocation = { ...mockLocation, isOccupied: false }
    expect(renderCell("isOccupied", availablePot).text()).toBe("Available")
  })

  it("isOccupied column renders Occupied badge for an occupied pot", () => {
    const occupiedPot: PlantingLocation = { ...mockLocation, isOccupied: true }
    expect(renderCell("isOccupied", occupiedPot).text()).toBe("Occupied")
  })

  it("isOccupied column renders Available badge for an unoccupied nursery pot", () => {
    const availableNurseryPot: PlantingLocation = {
      ...mockLocation,
      locationType: "NURSERYPOT",
      isOccupied: false,
    }
    expect(renderCell("isOccupied", availableNurseryPot).text()).toBe("Available")
  })

  it("isOccupied column renders Occupied badge for an occupied nursery pot", () => {
    const occupiedNurseryPot: PlantingLocation = {
      ...mockLocation,
      locationType: "NURSERYPOT",
      isOccupied: true,
    }
    expect(renderCell("isOccupied", occupiedNurseryPot).text()).toBe("Occupied")
  })

  it("isOccupied column renders dash for ground locations", () => {
    expect(renderCell("isOccupied", mockLocationNoOptionals).text()).toBe("-")
  })

  it("actions column cell type is PlantingLocationTableActions", () => {
    expect(getVnode("actions").type).toBe(PlantingLocationTableActions)
  })
})
