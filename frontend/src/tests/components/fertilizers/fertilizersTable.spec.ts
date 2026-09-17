import { mount } from "@vue/test-utils"
import { describe, it, expect } from "vitest"
import FertilizersTable from "@/components/fertilizers/FertilizersTable.vue"
import type { Fertilizer } from "@/types/fertilizer"

const mockFertilizers: Fertilizer[] = [
  {
    id: 1,
    name: "Swamp Fertilizer #1",
    type: "SWAMP",
    status: "BREWING",
    startDate: "2024-01-01",
    ingredients: ["banana peels"],
    notes: "",
    createdAt: "2024-01-01T00:00:00Z",
    updatedAt: "2024-01-01T00:00:00Z",
  },
]

const stubs = {
  BaseDataTable: {
    template: "<div data-stub='base-table' />",
    props: ["tableData", "columns", "rowCount", "pagination", "searchTerm"],
    emits: ["update:searchTerm", "pagination-change", "delete", "update", "action"],
  },
}

describe("FertilizersTable.vue", () => {
  it("renders BaseDataTable", () => {
    const wrapper = mount(FertilizersTable, {
      props: { data: mockFertilizers, rowCount: 1, pagination: { pageIndex: 0, pageSize: 10 } },
      global: { stubs },
    })

    expect(wrapper.find("[data-stub='base-table']").exists()).toBe(true)
  })
})
