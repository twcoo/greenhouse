import { mount } from "@vue/test-utils"
import { describe, it, expect } from "vitest"
import PlantingLocationTable from "@/components/planting-locations/PlantingLocationTable.vue"
import type { PlantingLocation } from "@/types/plantingLocation"

const mockLocations: PlantingLocation[] = [
  {
    id: 1,
    name: "Garden Pot",
    locationType: "POT",
    width: 30,
    height: 40,
  },
]

const stubs = {
  BaseDataTable: {
    template: "<div data-stub='base-table' />",
    props: ["tableData", "columns", "filterableColumns", "rowCount", "pagination", "searchTerm"],
    emits: ["update:searchTerm", "pagination-change", "delete", "update"],
  },
}

describe("PlantingLocationTable.vue", () => {
  it("renders BaseDataTable", () => {
    const wrapper = mount(PlantingLocationTable, {
      props: { data: mockLocations, rowCount: 1, pagination: { pageIndex: 0, pageSize: 10 } },
      global: { stubs },
    })

    expect(wrapper.find("[data-stub='base-table']").exists()).toBe(true)
  })

  it("renders without errors when given location data", () => {
    const wrapper = mount(PlantingLocationTable, {
      props: { data: mockLocations, rowCount: 1, pagination: { pageIndex: 0, pageSize: 10 } },
      global: { stubs },
    })

    expect(wrapper.find("[data-stub='base-table']").exists()).toBe(true)
  })
})
