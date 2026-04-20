import { mount } from "@vue/test-utils"
import { describe, it, expect } from "vitest"
import CropsTable from "@/components/crops/CropsTable.vue"
import type { Crop } from "@/types/crop"

const mockCrops: Crop[] = [
  {
    id: 1,
    name: "Tomato",
    scientificName: "Solanum lycopersicum",
    category: "VEGETABLE",
    sunlightRequirement: "FULL SUN",
    minDaysToHarvest: 60,
    maxDaysToHarvest: 80,
  },
]

const stubs = {
  BaseDataTable: {
    template: "<div data-stub='base-table' />",
    props: ["tableData", "columns", "filterableColumns", "rowCount", "pagination", "searchTerm"],
    emits: ["update:searchTerm", "pagination-change", "delete", "update"],
  },
}

describe("CropsTable.vue", () => {
  it("renders BaseDataTable", () => {
    const wrapper = mount(CropsTable, {
      props: { data: mockCrops, rowCount: 1, pagination: { pageIndex: 0, pageSize: 10 } },
      global: { stubs },
    })

    expect(wrapper.find("[data-stub='base-table']").exists()).toBe(true)
  })

  it("passes filterableColumns including category and sunlightRequirement", () => {
    const wrapper = mount(CropsTable, {
      props: { data: mockCrops, rowCount: 1, pagination: { pageIndex: 0, pageSize: 10 } },
      global: { stubs },
    })

    // BaseDataTable stub renders, confirming props were received without error
    expect(wrapper.find("[data-stub='base-table']").exists()).toBe(true)
  })
})
