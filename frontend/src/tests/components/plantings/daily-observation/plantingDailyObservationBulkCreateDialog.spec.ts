import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import PlantingDailyObservationBulkCreateDialog from "@/components/plantings/daily-observation/PlantingDailyObservationBulkCreateDialog.vue"
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
  {
    id: 2,
    crop: 2,
    cropName: "Pepper",
    variety: 2,
    varietyName: "Bell",
    createdAt: "2024-02-01T00:00:00Z",
  },
]

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
      '<input data-stub="select" :value="modelValue" @input="$emit(\'update:modelValue\', $event.target.value)" />',
    props: ["modelValue"],
    emits: ["update:modelValue"],
  },
  SelectTrigger: { template: "<span />" },
  SelectContent: { template: "<span />" },
  SelectItem: { template: "<span />" },
  SelectValue: { template: "<span />" },
  Checkbox: {
    template:
      '<input type="checkbox" :checked="modelValue" @change="$emit(\'update:modelValue\', $event.target.checked)" />',
    props: ["modelValue"],
    emits: ["update:modelValue"],
  },
  Input: {
    template:
      '<input :value="modelValue" @input="$emit(\'update:modelValue\', $event.target.value)" />',
    props: ["modelValue"],
    emits: ["update:modelValue"],
  },
  FieldGroup: { template: "<div><slot /></div>" },
  Field: { template: "<div><slot /></div>" },
  FieldLabel: { template: "<label><slot /></label>" },
  FieldError: { template: "<span><slot /></span>" },
  Button: {
    template: "<button @click=\"$emit('click')\"><slot /></button>",
    emits: ["click"],
  },
  IconLoader2: { template: "<span />" },
  DatePicker: {
    template:
      '<input data-stub="date-picker" :value="modelValue" @input="$emit(\'update:modelValue\', $event.target.value)" />',
    props: ["modelValue"],
    emits: ["update:modelValue"],
  },
}

const mountComponent = (props = {}) =>
  mount(PlantingDailyObservationBulkCreateDialog, {
    props: {
      open: true,
      isLoading: false,
      isCreateSuccess: false,
      selectedPlantings: mockPlantings,
      ...props,
    },
    global: { stubs },
  })

beforeEach(() => {
  vi.clearAllMocks()
})

describe("PlantingDailyObservationBulkCreateDialog.vue", () => {
  describe("rendering", () => {
    it("shows the selected planting count in the title", () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain("2 Plantings")
    })

    it("shows planting summary with crop and variety names", () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain("Tomato (Sun Gold)")
      expect(wrapper.text()).toContain("Pepper (Bell)")
    })

    it("renders the observation date picker", () => {
      const wrapper = mountComponent()

      expect(wrapper.find('[data-stub="date-picker"]').exists()).toBe(true)
    })

    it("renders health status, pest pressure, watering event, and fertilizer type selects", () => {
      const wrapper = mountComponent()

      const selects = wrapper.findAll('[data-stub="select"]')
      expect(selects).toHaveLength(4)
    })

    it("renders the disease symptoms and pruned checkboxes", () => {
      const wrapper = mountComponent()

      expect(wrapper.findAll('input[type="checkbox"]')).toHaveLength(2)
    })

    it("renders the notes textarea", () => {
      const wrapper = mountComponent()

      expect(wrapper.find("#notes").exists()).toBe(true)
    })

    it("does not render an image input area", () => {
      const wrapper = mountComponent()

      expect(wrapper.find('[data-test="image-input-area"]').exists()).toBe(false)
    })

    it("shows Saving... on the submit button when isLoading is true", () => {
      const wrapper = mountComponent({ isLoading: true })

      expect(wrapper.text()).toContain("Saving...")
    })
  })

  describe("planting summary", () => {
    it("displays a single planting summary correctly", () => {
      const wrapper = mountComponent({ selectedPlantings: [mockPlantings[0]] })

      expect(wrapper.text()).toContain("Tomato (Sun Gold)")
    })

    it("updates the title for a single planting", () => {
      const wrapper = mountComponent({ selectedPlantings: [mockPlantings[0]] })

      expect(wrapper.text()).toContain("1 Plantings")
    })
  })

  describe("default form state", () => {
    it("defaults observationDate to today's date", () => {
      const today = new Date().toISOString().split("T")[0]
      const wrapper = mountComponent()

      const datePicker = wrapper.find('[data-stub="date-picker"]').element as HTMLInputElement
      expect(datePicker.value).toBe(today)
    })

    it("defaults healthStatus select to GOOD", () => {
      const wrapper = mountComponent()

      const selects = wrapper.findAll('[data-stub="select"]')
      expect((selects[0].element as HTMLInputElement).value).toBe("GOOD")
    })

    it("defaults pestPressure select to NONE", () => {
      const wrapper = mountComponent()

      const selects = wrapper.findAll('[data-stub="select"]')
      expect((selects[1].element as HTMLInputElement).value).toBe("NONE")
    })

    it("defaults wateringEvent select to empty", () => {
      const wrapper = mountComponent()

      const selects = wrapper.findAll('[data-stub="select"]')
      expect((selects[2].element as HTMLInputElement).value).toBe("")
    })

    it("defaults fertilizerType select to NONE", () => {
      const wrapper = mountComponent()

      const selects = wrapper.findAll('[data-stub="select"]')
      expect((selects[3].element as HTMLInputElement).value).toBe("NONE")
    })
  })

  describe("submission", () => {
    it("emits submit with default payload when form is valid", async () => {
      const today = new Date().toISOString().split("T")[0]
      const wrapper = mountComponent()

      await wrapper.find("form").trigger("submit.prevent")

      const emitted = wrapper.emitted("submit")
      expect(emitted).toBeDefined()
      const submittedPayload = emitted![0][0] as Record<string, unknown>
      expect(submittedPayload).toMatchObject({
        observationDate: today,
        healthStatus: "GOOD",
        pestPressure: "NONE",
        diseaseSymptoms: false,
        fertilizerType: "NONE",
        pruned: false,
      })
      expect(submittedPayload.wateringEvent).toBeUndefined()
    })

    it("emits submit with updated healthStatus when changed", async () => {
      const wrapper = mountComponent()

      await wrapper.findAll('[data-stub="select"]')[0].setValue("POOR")
      await wrapper.find("form").trigger("submit.prevent")

      const submittedPayload = wrapper.emitted("submit")![0][0] as Record<string, unknown>
      expect(submittedPayload.healthStatus).toBe("POOR")
    })

    it("does not emit submit when healthStatus is invalid", async () => {
      const wrapper = mountComponent()

      await wrapper.findAll('[data-stub="select"]')[0].setValue("")
      await wrapper.find("form").trigger("submit.prevent")

      expect(wrapper.emitted("submit")).toBeUndefined()
    })

    it("shows healthStatus field error on invalid submit", async () => {
      const wrapper = mountComponent()

      await wrapper.findAll('[data-stub="select"]')[0].setValue("")
      await wrapper.find("form").trigger("submit.prevent")

      expect(wrapper.find('[data-test="healthStatusError"]').exists()).toBe(true)
    })
  })

  describe("error handling via onError callback", () => {
    it("shows field errors from API response", async () => {
      const wrapper = mountComponent()

      await wrapper.find("form").trigger("submit.prevent")

      const onError = wrapper.emitted("submit")![0][1] as (err: unknown) => void
      onError({
        response: {
          data: { message: { healthStatus: ["Invalid choice."] } },
        },
      })
      await wrapper.vm.$nextTick()

      expect(wrapper.find('[data-test="healthStatusError"]').exists()).toBe(true)
    })

    it("shows general error when API call fails without response data", async () => {
      const wrapper = mountComponent()

      await wrapper.find("form").trigger("submit.prevent")

      const onError = wrapper.emitted("submit")![0][1] as (err: unknown) => void
      onError(new Error("Network error"))
      await wrapper.vm.$nextTick()

      expect(wrapper.find('[data-test="general-error"]').text()).toContain(
        "Something went wrong. Please try again.",
      )
    })
  })

  describe("close on success", () => {
    it("emits update:open false when isCreateSuccess becomes true", async () => {
      const wrapper = mountComponent({ isCreateSuccess: false })

      await wrapper.setProps({ isCreateSuccess: true })

      const openEvents = wrapper.emitted("update:open")
      expect(openEvents).toBeDefined()
      expect(openEvents?.[openEvents.length - 1][0]).toBe(false)
    })
  })

  describe("form reset", () => {
    it("resets observationDate to today when dialog is closed and reopened", async () => {
      const today = new Date().toISOString().split("T")[0]
      const wrapper = mountComponent()

      await wrapper.find('[data-stub="date-picker"]').setValue("2020-01-01")
      await wrapper.setProps({ open: false })
      await wrapper.vm.$nextTick()
      await wrapper.setProps({ open: true })
      await wrapper.vm.$nextTick()

      const datePicker = wrapper.find('[data-stub="date-picker"]').element as HTMLInputElement
      expect(datePicker.value).toBe(today)
    })

    it("clears field errors when dialog is closed and reopened", async () => {
      const wrapper = mountComponent()

      await wrapper.findAll('[data-stub="select"]')[0].setValue("")
      await wrapper.find("form").trigger("submit.prevent")
      expect(wrapper.find('[data-test="healthStatusError"]').exists()).toBe(true)

      await wrapper.setProps({ open: false })
      await wrapper.vm.$nextTick()
      await wrapper.setProps({ open: true })
      await wrapper.vm.$nextTick()

      expect(wrapper.find('[data-test="healthStatusError"]').exists()).toBe(false)
    })
  })
})
