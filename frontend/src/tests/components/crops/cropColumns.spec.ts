import { describe, it, expect, vi } from "vitest"
import { defineComponent } from "vue"
import { mount } from "@vue/test-utils"
import { columns } from "@/components/crops/CropColumns"
import CropTableActions from "@/components/crops/CropTableActions.vue"
import type { Crop } from "@/types/crop"

const mockCrop: Crop = {
  id: 1,
  name: "Tomato",
  scientificName: "Solanum lycopersicum",
  category: "VEGETABLE",
  sunlightRequirement: "FULL SUN",
  minDaysToHarvest: 60,
  maxDaysToHarvest: 80,
}

const mockRow = {
  getValue: (key: string) => mockCrop[key as keyof Crop],
  original: mockCrop,
}

const mockTable = {
  options: { meta: { update: vi.fn(), delete: vi.fn() } },
}

function getVnode(colId: string) {
  const col = columns.find((c) => c.id === colId)!
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  return (col as any).cell({ row: mockRow, table: mockTable })
}

function renderCell(colId: string) {
  const vnode = getVnode(colId)
  return mount(defineComponent({ render: () => vnode }))
}

describe("CropColumns", () => {
  it("name column renders crop name", () => {
    expect(renderCell("name").text()).toBe("Tomato")
  })

  it("scientificName column renders scientific name", () => {
    expect(renderCell("scientificName").text()).toBe("Solanum lycopersicum")
  })

  it("minDaysToHarvest column renders value as string", () => {
    expect(renderCell("minDaysToHarvest").text()).toBe("60")
  })

  it("maxDaysToHarvest column renders value as string", () => {
    expect(renderCell("maxDaysToHarvest").text()).toBe("80")
  })

  it("actions column cell type is CropTableActions", () => {
    expect(getVnode("actions").type).toBe(CropTableActions)
  })
})
