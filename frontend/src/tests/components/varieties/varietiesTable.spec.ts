import { mount } from "@vue/test-utils"
import { describe, it, expect } from "vitest"
import VarietiesTable from "@/components/varieties/VarietiesTable.vue"
import type { Variety } from "@/types/variety"

const mockVarieties: Variety[] = [
  {
    id: 1,
    name: "Sun Gold",
    crop: 1,
    cropName: "Tomato",
    growthHabit: ["INDETERMINATE"],
  },
]

const stubs = {
  BaseDataTable: {
    template: "<div data-stub='base-table' />",
    props: ["tableData", "columns", "rowCount", "pagination", "searchTerm"],
    emits: ["update:searchTerm", "pagination-change", "delete", "update"],
  },
}

describe("VarietiesTable.vue", () => {
  it("renders BaseDataTable", () => {
    const wrapper = mount(VarietiesTable, {
      props: { data: mockVarieties, rowCount: 1, pagination: { pageIndex: 0, pageSize: 10 } },
      global: { stubs },
    })

    expect(wrapper.find("[data-stub='base-table']").exists()).toBe(true)
  })

  it("renders without errors when given variety data", () => {
    const wrapper = mount(VarietiesTable, {
      props: { data: mockVarieties, rowCount: 1, pagination: { pageIndex: 0, pageSize: 10 } },
      global: { stubs },
    })

    expect(wrapper.find("[data-stub='base-table']").exists()).toBe(true)
  })
})
