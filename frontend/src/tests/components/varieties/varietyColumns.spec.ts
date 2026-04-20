import { describe, it, expect, vi } from "vitest"
import { defineComponent } from "vue"
import { mount } from "@vue/test-utils"
import { columns } from "@/components/varieties/VarietyColumns"
import VarietyTableActions from "@/components/varieties/VarietyTableActions.vue"
import type { Variety } from "@/types/variety"

const mockVariety: Variety = {
  id: 1,
  name: "Sun Gold",
  crop: 1,
  cropName: "Tomato",
  growthHabit: ["DETERMINATE", "INDETERMINATE"],
}

const mockRow = {
  getValue: (key: string) => mockVariety[key as keyof Variety],
  original: mockVariety,
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

describe("VarietyColumns", () => {
  it("name column renders variety name", () => {
    expect(renderCell("name").text()).toBe("Sun Gold")
  })

  it("cropName column renders crop name", () => {
    expect(renderCell("cropName").text()).toBe("Tomato")
  })

  it("growthHabit column returns one child vnode per habit", () => {
    const vnode = getVnode("growthHabit")
    // children is the array of Badge vnodes mapped from growthHabit values
    expect(Array.isArray(vnode.children)).toBe(true)
    expect((vnode.children as unknown[]).length).toBe(2)
  })

  it("actions column cell type is VarietyTableActions", () => {
    expect(getVnode("actions").type).toBe(VarietyTableActions)
  })
})
