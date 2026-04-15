import { mount } from "@vue/test-utils"
import { describe, it, expect } from "vitest"
import BaseDataTable from "@/components/BaseDataTable.vue"
import type { ColumnDef } from "@tanstack/vue-table"
import type { PaginationState } from "@/types/pagination"

interface SampleData {
  id: number
  name: string
  status: string
}

describe("BaseDataTable.vue", () => {
  const sampleData: SampleData[] = [
    { id: 1, name: "Alpha", status: "Active" },
    { id: 2, name: "Beta", status: "Inactive" },
    { id: 3, name: "Gamma", status: "Active" },
  ]

  const sampleColumns: ColumnDef<SampleData>[] = [
    { accessorKey: "id", header: "ID" },
    { accessorKey: "name", header: "Name" },
    { accessorKey: "status", header: "Status" },
  ]

  const samplePagination: PaginationState = {
    pageIndex: 0,
    pageSize: 5,
  }

  const mountComponent = (
    props = {
      tableData: sampleData,
      columns: sampleColumns,
      rowCount: sampleData.length,
      pagination: samplePagination,
    },
  ) => {
    return mount(BaseDataTable<SampleData>, {
      props,
      global: {
        stubs: {
          Table: { template: "<table><slot /></table>" },
          TableHeader: { template: "<thead><slot /></thead>" },
          TableBody: { template: "<tbody><slot /></tbody>" },
          TableRow: { template: "<tr><slot /></tr>" },
          TableHead: { template: "<th><slot /></th>" },
          TableCell: { template: "<td><slot /></td>" },
          Button: { template: "<button @click=\"$emit('click')\"><slot /></button>" },
          Select: { template: "<div><slot /></div>" },
          SelectTrigger: { template: "<div><slot /></div>" },
          SelectValue: { template: "<div><slot /></div>" },
          SelectContent: { template: "<div><slot /></div>" },
          SelectGroup: { template: "<div><slot /></div>" },
          SelectItem: { template: "<div><slot /></div>" },
          Input: {
            template:
              '<input @input="$emit(\'update:modelValue\', ($event.target).value)" :value="modelValue" />',
          },
          Label: { template: "<div><slot /></div>" },
          IconGhost2: { template: "<svg />" },
        },
      },
    })
  }

  it("renders the table headers and data correctly", () => {
    const wrapper = mountComponent()

    // Headers
    const headers = wrapper.findAll("th")
    expect(headers).toHaveLength(sampleColumns.length)
    expect(headers[0].text()).toBe("ID")
    expect(headers[1].text()).toBe("Name")
    expect(headers[2].text()).toBe("Status")

    // Data rows
    const rows = wrapper.findAll("tbody tr")
    expect(rows).toHaveLength(sampleData.length)

    // Data cells for the first row
    const firstRowCells = rows[0].findAll("td")
    expect(firstRowCells[0].text()).toBe("1")
    expect(firstRowCells[1].text()).toBe("Alpha")
    expect(firstRowCells[2].text()).toBe("Active")
  })

  it("emits 'pagination-change' when 'Next' button is clicked", async () => {
    const wrapper = mountComponent({
      tableData: sampleData,
      columns: sampleColumns,
      rowCount: 10,
      pagination: samplePagination,
    })

    const nextButton = wrapper.findAll("button").find((b) => b.text().includes("Next"))
    expect(nextButton).toBeDefined()

    await nextButton?.trigger("click")

    const event = wrapper.emitted("pagination-change")
    expect(event).toBeDefined()
    expect(event?.[0][0]).toEqual({
      pageIndex: 1,
      pageSize: 5,
    })
  })

  it("disables 'Previous' and 'Next' buttons correctly", () => {
    // 1. Test first page: Previous should be disabled, Next should be enabled (if more data exists)
    let wrapper = mountComponent({
      tableData: sampleData,
      columns: sampleColumns,
      rowCount: 10,
      pagination: { pageIndex: 0, pageSize: 5 },
    })

    let buttons = wrapper.findAll("button")
    let prevButton = buttons.find((b) => b.text().includes("Previous"))
    let nextButton = buttons.find((b) => b.text().includes("Next"))

    expect(prevButton?.element.disabled).toBe(true)
    expect(nextButton?.element.disabled).toBe(false)

    // 2. Test last page: Previous should be enabled, Next should be disabled
    wrapper = mountComponent({
      tableData: sampleData,
      columns: sampleColumns,
      rowCount: 10,
      pagination: { pageIndex: 1, pageSize: 5 },
    })

    buttons = wrapper.findAll("button")
    prevButton = buttons.find((b) => b.text().includes("Previous"))
    nextButton = buttons.find((b) => b.text().includes("Next"))

    expect(prevButton?.element.disabled).toBe(false)
    expect(nextButton?.element.disabled).toBe(true)

    // 3. Test only one page: Both should be disabled
    wrapper = mountComponent({
      tableData: sampleData,
      columns: sampleColumns,
      rowCount: 3,
      pagination: { pageIndex: 0, pageSize: 5 },
    })

    buttons = wrapper.findAll("button")
    prevButton = buttons.find((b) => b.text().includes("Previous"))
    nextButton = buttons.find((b) => b.text().includes("Next"))

    expect(prevButton?.element.disabled).toBe(true)
    expect(nextButton?.element.disabled).toBe(true)
  })

  it("calculates page range correctly", () => {
    const wrapper = mountComponent({
      tableData: sampleData,
      columns: sampleColumns,
      rowCount: 50,
      pagination: { pageIndex: 0, pageSize: 5 },
    })

    const pageButtons = wrapper.findAll(".hidden.sm\\:flex button")
    expect(pageButtons).toHaveLength(5)
    expect(pageButtons[0].text()).toBe("1")
    expect(pageButtons[4].text()).toBe("5")
  })

  it("handles empty data state", () => {
    const wrapper = mountComponent({
      tableData: [],
      columns: sampleColumns,
      rowCount: 0,
      pagination: samplePagination,
    })

    expect(wrapper.text()).toContain("No data available.")
  })

  it("handles empty results search state", async () => {
    const wrapper = mountComponent({
      tableData: [],
      columns: sampleColumns,
      rowCount: 0,
      pagination: samplePagination,
    })

    const input = wrapper.find("input")
    await input.setValue("unknown")

    expect(wrapper.text()).toContain("No results found.")
  })
})
