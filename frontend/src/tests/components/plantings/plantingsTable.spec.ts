import { mount } from "@vue/test-utils"
import { describe, it, expect } from "vitest"
import PlantingsTable from "@/components/plantings/PlantingsTable.vue"
import type { Planting } from "@/types/planting"

const mockPlantings: Planting[] = [
  {
    id: 1,
    crop: 1,
    cropName: "Tomato",
    variety: 1,
    varietyName: "Sun Gold",
    createdAt: "2024-01-01T00:00:00Z",
  },
]

const stubs = {
  BaseDataTable: {
    template: "<div data-stub='base-table' />",
    props: ["tableData", "columns", "rowCount", "pagination", "searchTerm"],
    emits: ["update:searchTerm", "pagination-change", "delete", "update"],
  },
}

describe("PlantingsTable.vue", () => {
  it("renders BaseDataTable", () => {
    const wrapper = mount(PlantingsTable, {
      props: {
        data: mockPlantings,
        rowCount: 1,
        pagination: { pageIndex: 0, pageSize: 10 },
      },
      global: { stubs },
    })

    expect(wrapper.find("[data-stub='base-table']").exists()).toBe(true)
  })

  it("renders without errors when given empty data", () => {
    const wrapper = mount(PlantingsTable, {
      props: { data: [], rowCount: 0, pagination: { pageIndex: 0, pageSize: 10 } },
      global: { stubs },
    })

    expect(wrapper.find("[data-stub='base-table']").exists()).toBe(true)
  })
})
