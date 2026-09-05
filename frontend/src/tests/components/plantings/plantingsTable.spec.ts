import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import PlantingsTable from "@/components/plantings/PlantingsTable.vue"
import type { Planting } from "@/types/planting"

const mockPlantings: Planting[] = [
  {
    id: 1,
    crop: 1,
    cropName: "Tomato",
    variety: 1,
    varietyName: "Sun Gold",
    status: "ACTIVE",
    currentLocation: null,
    hasDailyObservation: false,
    createdAt: "2024-01-01T00:00:00Z",
  },
  {
    id: 2,
    crop: 1,
    cropName: "Pepper",
    variety: 2,
    varietyName: "Bell",
    status: "ACTIVE",
    currentLocation: null,
    hasDailyObservation: false,
    createdAt: "2024-02-01T00:00:00Z",
  },
]

const stubs = {
  Table: { template: "<table><slot /></table>" },
  TableHeader: { template: "<thead><slot /></thead>" },
  TableBody: { template: "<tbody><slot /></tbody>" },
  TableRow: { template: "<tr><slot /></tr>" },
  TableHead: { template: "<th><slot /></th>" },
  TableCell: { template: "<td><slot /></td>" },
  Checkbox: {
    template:
      '<input type="checkbox" :checked="modelValue" @change="$emit(\'update:modelValue\', $event.target.checked)" />',
    props: ["modelValue"],
    emits: ["update:modelValue"],
  },
  Button: {
    template: "<button :disabled='disabled' @click=\"$emit('click')\"><slot /></button>",
    props: ["disabled", "size", "variant"],
    emits: ["click"],
  },
  Select: { template: "<div><slot /></div>" },
  SelectGroup: { template: "<div><slot /></div>" },
  SelectTrigger: { template: "<div><slot /></div>" },
  SelectValue: { template: "<div><slot /></div>" },
  SelectContent: { template: "<div><slot /></div>" },
  SelectItem: { template: "<div><slot /></div>" },
  Input: {
    template:
      '<input :value="modelValue" @input="$emit(\'update:modelValue\', $event.target.value)" />',
    props: ["modelValue"],
    emits: ["update:modelValue"],
  },
  Label: { template: "<div><slot /></div>" },
  IconGhost2: { template: "<svg />" },
  IconNotebook: { template: "<svg />" },
  PlantingTableActions: { template: "<div />" },
  Badge: { template: "<span><slot /></span>" },
}

const mountComponent = (props = {}) =>
  mount(PlantingsTable, {
    props: {
      data: mockPlantings,
      rowCount: mockPlantings.length,
      pagination: { pageIndex: 0, pageSize: 10 },
      ...props,
    },
    global: { stubs },
  })

beforeEach(() => {
  vi.clearAllMocks()
})

describe("PlantingsTable.vue", () => {
  it("renders a row for each planting", () => {
    const wrapper = mountComponent()

    expect(wrapper.findAll("tbody tr")).toHaveLength(mockPlantings.length)
  })

  it("renders empty state message when no data", () => {
    const wrapper = mountComponent({ data: [], rowCount: 0 })

    expect(wrapper.text()).toContain("No data available.")
  })

  it("renders a checkbox in each data row", () => {
    const wrapper = mountComponent()

    const rowCheckboxes = wrapper.findAll("tbody input[type='checkbox']")
    expect(rowCheckboxes).toHaveLength(mockPlantings.length)
  })

  it("renders a select-all checkbox in the table header", () => {
    const wrapper = mountComponent()

    const headerCheckboxes = wrapper.findAll("thead input[type='checkbox']")
    expect(headerCheckboxes).toHaveLength(1)
  })

  it("does not show bulk action toolbar when no rows are selected", () => {
    const wrapper = mountComponent()

    expect(wrapper.text()).not.toContain("selected")
    expect(wrapper.text()).not.toContain("Record Observation")
  })

  it("shows bulk action toolbar with count after a row is selected", async () => {
    const wrapper = mountComponent()

    const rowCheckbox = wrapper.findAll("tbody input[type='checkbox']")[0]
    ;(rowCheckbox.element as HTMLInputElement).checked = true
    await rowCheckbox.trigger("change")

    expect(wrapper.text()).toContain("1 selected")
    expect(wrapper.text()).toContain("Record Observation")
  })

  it("updates selected count when a second row is selected", async () => {
    const wrapper = mountComponent()

    for (const cb of wrapper.findAll("tbody input[type='checkbox']")) {
      ;(cb.element as HTMLInputElement).checked = true
      await cb.trigger("change")
    }

    expect(wrapper.text()).toContain("2 selected")
  })

  it("emits bulk-observe with the selected planting ID when Record Observation is clicked", async () => {
    const wrapper = mountComponent()

    const rowCheckbox = wrapper.findAll("tbody input[type='checkbox']")[0]
    ;(rowCheckbox.element as HTMLInputElement).checked = true
    await rowCheckbox.trigger("change")

    const recordBtn = wrapper.findAll("button").find((b) => b.text().includes("Record Observation"))
    await recordBtn!.trigger("click")

    expect(wrapper.emitted("bulk-observe")).toBeDefined()
    expect(wrapper.emitted("bulk-observe")![0][0]).toEqual([mockPlantings[0].id])
  })

  it("emits bulk-observe with all selected planting IDs", async () => {
    const wrapper = mountComponent()

    for (const cb of wrapper.findAll("tbody input[type='checkbox']")) {
      ;(cb.element as HTMLInputElement).checked = true
      await cb.trigger("change")
    }

    const recordBtn = wrapper.findAll("button").find((b) => b.text().includes("Record Observation"))
    await recordBtn!.trigger("click")

    const emittedIds = wrapper.emitted("bulk-observe")![0][0] as number[]
    expect(emittedIds).toHaveLength(mockPlantings.length)
    expect(emittedIds).toContain(mockPlantings[0].id)
    expect(emittedIds).toContain(mockPlantings[1].id)
  })
})
