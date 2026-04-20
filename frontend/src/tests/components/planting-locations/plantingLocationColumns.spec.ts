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
}

const mockLocationNoOptionals: PlantingLocation = {
  id: 2,
  name: "Garden Bed",
  locationType: "GROUND",
  width: 100,
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
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  return (col as any).cell({ row: mockRow, table: mockTable })
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

  it("actions column cell type is PlantingLocationTableActions", () => {
    expect(getVnode("actions").type).toBe(PlantingLocationTableActions)
  })
})
