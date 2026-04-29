import { ref } from "vue"
import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import PlantingLocationAssignmentUpdateDialog from "@/components/planting-location-assignments/PlantingLocationAssignmentUpdateDialog.vue"
import { createTestingPinia } from "@pinia/testing"
import type { PlantingLocationAssignmentForm } from "@/schemas/plantingLocationAssignment.schemas"

vi.mock("@/composables/usePlantingLocations", () => ({
  usePlantingLocations: vi.fn(() => ({
    locations: ref({
      results: [
        {
          id: 1,
          name: "Balcony Pot",
          locationType: "POT",
          width: 25,
          height: 30,
          currentStatus: null,
        },
        {
          id: 2,
          name: "Nursery Pot A",
          locationType: "NURSERYPOT",
          width: 15,
          height: 20,
          currentStatus: {
            id: 1,
            status: "IN_USE",
            notes: "",
            image: null,
            createdAt: "2024-01-01T00:00:00Z",
          },
        },
        {
          id: 3,
          name: "Occupied Pot",
          locationType: "POT",
          width: 20,
          height: 25,
          currentStatus: {
            id: 2,
            status: "IN_USE",
            notes: "",
            image: null,
            createdAt: "2024-01-01T00:00:00Z",
          },
        },
        {
          id: 4,
          name: "Garden Bed",
          locationType: "GROUND",
          width: 100,
          currentStatus: null,
        },
      ],
      count: 4,
    }),
  })),
}))

const stubs = {
  Dialog: { template: "<div><slot /></div>" },
  DialogContent: { template: "<div><slot /></div>" },
  DialogHeader: { template: "<div><slot /></div>" },
  DialogTitle: { template: "<div><slot /></div>" },
  DialogDescription: { template: "<div><slot /></div>" },
  DialogFooter: { template: "<div><slot /></div>" },
  DialogClose: { template: "<button><slot /></button>" },
  Select: {
    template:
      '<div><input data-stub="select" :value="modelValue" @input="$emit(\'update:modelValue\', $event.target.value)" /><slot /></div>',
    props: ["modelValue"],
    emits: ["update:modelValue"],
  },
  SelectTrigger: { template: "<span />" },
  SelectContent: { template: "<div><slot /></div>" },
  SelectValue: { template: "<span />" },
  SelectItem: {
    template: '<button :disabled="disabled" :data-value="value"><slot /></button>',
    props: ["value", "disabled"],
  },
  DatePicker: {
    template:
      '<input :placeholder="placeholder" :value="modelValue" @input="$emit(\'update:modelValue\', $event.target.value)" />',
    props: ["modelValue", "placeholder"],
    emits: ["update:modelValue"],
  },
}

// id=2 (Nursery Pot A) is the currently assigned location
const defaultInitialState: PlantingLocationAssignmentForm = {
  plantingLocation: 2,
  startDate: "2024-01-01",
  endDate: "2024-06-01",
}

const mountComponent = (props = {}) =>
  mount(PlantingLocationAssignmentUpdateDialog, {
    props: {
      open: true,
      id: 10,
      assignmentFormInitialState: defaultInitialState,
      isLoading: false,
      isUpdateSuccess: false,
      ...props,
    },
    global: {
      plugins: [createTestingPinia({ createSpy: vi.fn })],
      stubs,
    },
  })

beforeEach(() => {
  vi.clearAllMocks()
})

describe("PlantingLocationAssignmentUpdateDialog.vue", () => {
  it("pre-populates the select and date pickers from initial state", () => {
    const wrapper = mountComponent()

    const select = wrapper.find('[data-stub="select"]').element as HTMLInputElement
    expect(select.value).toBe("2")

    const startDate = wrapper.find('[placeholder="Pick a start date"]').element as HTMLInputElement
    expect(startDate.value).toBe("2024-01-01")

    const endDate = wrapper.find('[placeholder="Pick an end date"]').element as HTMLInputElement
    expect(endDate.value).toBe("2024-06-01")
  })

  it("emits submit with id, payload, and onError callback on valid form", async () => {
    const wrapper = mountComponent()

    await wrapper.find('[placeholder="Pick an end date"]').setValue("2024-09-01")
    await wrapper.find("form").trigger("submit.prevent")

    const emitted = wrapper.emitted("submit")
    expect(emitted).toBeDefined()
    expect(emitted?.[0][0]).toBe(10)
    expect(emitted?.[0][1]).toMatchObject({
      plantingLocation: 2,
      startDate: "2024-01-01",
      endDate: "2024-09-01",
    })
    expect(typeof emitted?.[0][2]).toBe("function")
  })

  it("shows validation error when start date is cleared", async () => {
    const wrapper = mountComponent()

    await wrapper.find('[data-stub="select"]').setValue("1")
    await wrapper.find('[placeholder="Pick a start date"]').setValue("")
    await wrapper.find("form").trigger("submit.prevent")

    expect(wrapper.find('[data-test="startDateError"]').exists()).toBe(true)
  })

  it("shows planting_location field error returned from the API", async () => {
    const wrapper = mountComponent()

    await wrapper.find("form").trigger("submit.prevent")

    const onError = wrapper.emitted("submit")?.[0][2] as (err: unknown) => void
    // The Axios interceptor converts snake_case to camelCase before error
    // handling, so by the time apiToFormErrors runs the key is camelCase.
    onError({
      response: {
        data: {
          message: {
            plantingLocation: [
              "This location already has an active planting for the given date range.",
            ],
          },
        },
      },
    })
    await wrapper.vm.$nextTick()

    expect(wrapper.find('[data-test="plantingLocationError"]').exists()).toBe(true)
  })

  it("shows general error when API call fails without a response body", async () => {
    const wrapper = mountComponent()

    await wrapper.find("form").trigger("submit.prevent")

    const onError = wrapper.emitted("submit")?.[0][2] as (err: unknown) => void
    onError(new Error("Network error"))
    await wrapper.vm.$nextTick()

    expect(wrapper.find('[data-test="general-error"]').exists()).toBe(true)
  })

  it("does not disable the currently assigned occupied location", () => {
    const wrapper = mountComponent()

    // id=2 is the currently assigned NURSERYPOT and is occupied — must remain enabled
    expect(wrapper.find('button[data-value="2"]').attributes("disabled")).toBeUndefined()
  })

  it("disables occupied pot locations that are not the current assignment", () => {
    const wrapper = mountComponent()

    // id=3 is an occupied POT that is NOT the current assignment — must be disabled
    expect(wrapper.find('button[data-value="3"]').attributes("disabled")).toBeDefined()
  })

  it("does not disable available pot locations", () => {
    const wrapper = mountComponent()

    expect(wrapper.find('button[data-value="1"]').attributes("disabled")).toBeUndefined()
  })

  it("does not disable ground locations", () => {
    const wrapper = mountComponent()

    expect(wrapper.find('button[data-value="4"]').attributes("disabled")).toBeUndefined()
  })

  it("shows loading text on button when isLoading is true", () => {
    const wrapper = mountComponent({ isLoading: true })

    const buttons = wrapper.findAll("button")
    const saveButton = buttons.find((b) => b.text().includes("Saving"))
    expect(saveButton).toBeDefined()
    expect(saveButton?.attributes("disabled")).toBeDefined()
  })

  it("closes dialog when isUpdateSuccess becomes true", async () => {
    const wrapper = mountComponent({ isUpdateSuccess: false })

    await wrapper.setProps({ isUpdateSuccess: true })

    const openEvents = wrapper.emitted("update:open")
    expect(openEvents).toBeDefined()
    expect(openEvents?.[openEvents.length - 1][0]).toBe(false)
  })

  it("clears errors when dialog is closed and reopened", async () => {
    const wrapper = mountComponent()

    await wrapper.find('[data-stub="select"]').setValue("0")
    await wrapper.find('[placeholder="Pick a start date"]').setValue("")
    await wrapper.find("form").trigger("submit.prevent")
    expect(wrapper.find('[data-test="startDateError"]').exists()).toBe(true)

    await wrapper.setProps({ open: false })
    await wrapper.vm.$nextTick()
    await wrapper.setProps({ open: true })
    await wrapper.vm.$nextTick()

    expect(wrapper.find('[data-test="startDateError"]').exists()).toBe(false)
  })

  it("syncs form when assignmentFormInitialState prop changes", async () => {
    const wrapper = mountComponent()

    const newState: PlantingLocationAssignmentForm = {
      plantingLocation: 1,
      startDate: "2025-01-01",
      endDate: undefined,
    }
    await wrapper.setProps({ assignmentFormInitialState: newState })
    await wrapper.vm.$nextTick()

    const select = wrapper.find('[data-stub="select"]').element as HTMLInputElement
    expect(select.value).toBe("1")

    const startDate = wrapper.find('[placeholder="Pick a start date"]').element as HTMLInputElement
    expect(startDate.value).toBe("2025-01-01")
  })
})
