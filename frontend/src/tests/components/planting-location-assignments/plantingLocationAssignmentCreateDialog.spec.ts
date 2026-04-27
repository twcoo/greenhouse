import { ref } from "vue"
import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import PlantingLocationAssignmentCreateDialog from "@/components/planting-location-assignments/PlantingLocationAssignmentCreateDialog.vue"
import { createTestingPinia } from "@pinia/testing"

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
          isOccupied: false,
        },
        {
          id: 2,
          name: "Nursery Pot A",
          locationType: "NURSERYPOT",
          width: 15,
          height: 20,
          isOccupied: true,
        },
        {
          id: 3,
          name: "Garden Bed",
          locationType: "GROUND",
          width: 100,
          isOccupied: false,
        },
      ],
      count: 3,
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

const mountComponent = (props = {}) =>
  mount(PlantingLocationAssignmentCreateDialog, {
    props: {
      open: true,
      isLoading: false,
      isCreateSuccess: false,
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

describe("PlantingLocationAssignmentCreateDialog.vue", () => {
  it("renders location select and date pickers", () => {
    const wrapper = mountComponent()

    expect(wrapper.find('[data-stub="select"]').exists()).toBe(true)
    expect(wrapper.find('[placeholder="Pick a start date"]').exists()).toBe(true)
    expect(wrapper.find('[placeholder="Pick an end date"]').exists()).toBe(true)
  })

  it("shows validation error when no location is selected on submit", async () => {
    const wrapper = mountComponent()

    await wrapper.find('[placeholder="Pick a start date"]').setValue("2024-03-01")
    await wrapper.find("form").trigger("submit.prevent")

    expect(wrapper.find('[data-test="plantingLocationError"]').exists()).toBe(true)
  })

  it("shows validation error when no start date is provided", async () => {
    const wrapper = mountComponent()

    await wrapper.find('[data-stub="select"]').setValue("1")
    await wrapper.find("form").trigger("submit.prevent")

    expect(wrapper.find('[data-test="startDateError"]').exists()).toBe(true)
  })

  it("shows end date error when end date is before start date", async () => {
    const wrapper = mountComponent()

    await wrapper.find('[data-stub="select"]').setValue("1")
    await wrapper.find('[placeholder="Pick a start date"]').setValue("2024-06-01")
    await wrapper.find('[placeholder="Pick an end date"]').setValue("2024-01-01")
    await wrapper.find("form").trigger("submit.prevent")

    expect(wrapper.find('[data-test="endDateError"]').exists()).toBe(true)
  })

  it("emits submit with payload when form is valid", async () => {
    const wrapper = mountComponent()

    await wrapper.find('[data-stub="select"]').setValue("1")
    await wrapper.find('[placeholder="Pick a start date"]').setValue("2024-03-01")
    await wrapper.find("form").trigger("submit.prevent")

    const emitted = wrapper.emitted("submit")
    expect(emitted).toBeDefined()
    const payload = emitted![0][0] as Record<string, unknown>
    expect(payload).toMatchObject({
      plantingLocation: 1,
      startDate: "2024-03-01",
    })
    expect(payload.endDate).toBeUndefined()
  })

  it("includes endDate in payload when provided", async () => {
    const wrapper = mountComponent()

    await wrapper.find('[data-stub="select"]').setValue("1")
    await wrapper.find('[placeholder="Pick a start date"]').setValue("2024-03-01")
    await wrapper.find('[placeholder="Pick an end date"]').setValue("2024-09-01")
    await wrapper.find("form").trigger("submit.prevent")

    const emitted = wrapper.emitted("submit")
    expect(emitted?.[0][0]).toMatchObject({
      plantingLocation: 1,
      startDate: "2024-03-01",
      endDate: "2024-09-01",
    })
  })

  it("shows planting_location field error returned from the API", async () => {
    const wrapper = mountComponent()

    await wrapper.find('[data-stub="select"]').setValue("1")
    await wrapper.find('[placeholder="Pick a start date"]').setValue("2024-03-01")
    await wrapper.find("form").trigger("submit.prevent")

    const onError = wrapper.emitted("submit")?.[0][1] as (err: unknown) => void
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

    await wrapper.find('[data-stub="select"]').setValue("1")
    await wrapper.find('[placeholder="Pick a start date"]').setValue("2024-03-01")
    await wrapper.find("form").trigger("submit.prevent")

    const onError = wrapper.emitted("submit")?.[0][1] as (err: unknown) => void
    onError(new Error("Network error"))
    await wrapper.vm.$nextTick()

    expect(wrapper.find('[data-test="general-error"]').exists()).toBe(true)
  })

  it("shows loading text on button when isLoading is true", () => {
    const wrapper = mountComponent({ isLoading: true })

    const buttons = wrapper.findAll("button")
    const saveButton = buttons.find((b) => b.text().includes("Saving"))
    expect(saveButton).toBeDefined()
  })

  it("closes dialog when isCreateSuccess becomes true", async () => {
    const wrapper = mountComponent({ isCreateSuccess: false })

    await wrapper.setProps({ isCreateSuccess: true })

    const openEvents = wrapper.emitted("update:open")
    expect(openEvents).toBeDefined()
    expect(openEvents?.[openEvents.length - 1][0]).toBe(false)
  })

  it("resets form when dialog is closed", async () => {
    const wrapper = mountComponent()

    await wrapper.find('[data-stub="select"]').setValue("1")
    await wrapper.find('[placeholder="Pick a start date"]').setValue("2024-03-01")

    await wrapper.setProps({ open: false })
    await wrapper.vm.$nextTick()
    await wrapper.setProps({ open: true })
    await wrapper.vm.$nextTick()

    const select = wrapper.find('[data-stub="select"]').element as HTMLInputElement
    expect(select.value).toBe("")
  })

  it("disables occupied pot and nursery pot locations in the dropdown", () => {
    const wrapper = mountComponent()

    // Available POT (id=1) — must not be disabled
    expect(wrapper.find('button[data-value="1"]').attributes("disabled")).toBeUndefined()

    // Occupied NURSERYPOT (id=2) — must be disabled
    expect(wrapper.find('button[data-value="2"]').attributes("disabled")).toBeDefined()
  })

  it("does not disable ground locations regardless of occupied state", () => {
    const wrapper = mountComponent()

    expect(wrapper.find('button[data-value="3"]').attributes("disabled")).toBeUndefined()
  })

  it("shows (occupied) label for occupied pot/nursery pot locations", () => {
    const wrapper = mountComponent()

    expect(wrapper.find('button[data-value="2"]').text()).toContain("(occupied)")
  })

  it("does not show (occupied) label for available pot locations", () => {
    const wrapper = mountComponent()

    expect(wrapper.find('button[data-value="1"]').text()).not.toContain("(occupied)")
  })
})
