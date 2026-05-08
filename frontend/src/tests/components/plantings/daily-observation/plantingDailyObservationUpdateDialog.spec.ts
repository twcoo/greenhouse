import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import PlantingDailyObservationUpdateDialog from "@/components/plantings/daily-observation/PlantingDailyObservationUpdateDialog.vue"
import type { PlantingDailyObservationForm } from "@/schemas/plantingDailyObservation.schemas"

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
}

const baseInitialState: PlantingDailyObservationForm = {
  healthStatus: "FAIR",
  pestPressure: "LOW",
  diseaseSymptoms: false,
  heightCm: 20,
  leafCount: 5,
  temperatureC: undefined,
  humidityPercent: undefined,
  lightHours: undefined,
  soilMoisturePercent: undefined,
  soilPh: undefined,
  ecMsCm: undefined,
  notes: "Original notes",
  image: undefined,
}

const mountComponent = (props = {}) =>
  mount(PlantingDailyObservationUpdateDialog, {
    props: {
      open: true,
      id: 42,
      observationFormInitialState: baseInitialState,
      isLoading: false,
      isUpdateSuccess: false,
      ...props,
    },
    global: { stubs },
  })

beforeEach(() => {
  vi.clearAllMocks()
})

describe("PlantingDailyObservationUpdateDialog.vue", () => {
  describe("form pre-population", () => {
    it("pre-populates healthStatus from observationFormInitialState", () => {
      const wrapper = mountComponent()

      const selects = wrapper.findAll('[data-stub="select"]')
      expect((selects[0].element as HTMLInputElement).value).toBe("FAIR")
    })

    it("pre-populates pestPressure from observationFormInitialState", () => {
      const wrapper = mountComponent()

      const selects = wrapper.findAll('[data-stub="select"]')
      expect((selects[1].element as HTMLInputElement).value).toBe("LOW")
    })

    it("reflects diseaseSymptoms = false from observationFormInitialState", () => {
      const wrapper = mountComponent()

      const checkbox = wrapper.find('input[type="checkbox"]').element as HTMLInputElement
      expect(checkbox.checked).toBe(false)
    })

    it("reflects diseaseSymptoms = true from observationFormInitialState", () => {
      const wrapper = mountComponent({
        observationFormInitialState: { ...baseInitialState, diseaseSymptoms: true },
      })

      const checkbox = wrapper.find('input[type="checkbox"]').element as HTMLInputElement
      expect(checkbox.checked).toBe(true)
    })

    it("pre-populates notes from observationFormInitialState", () => {
      const wrapper = mountComponent()

      const notes = wrapper.find("#notes").element as HTMLTextAreaElement
      expect(notes.value).toBe("Original notes")
    })
  })

  describe("submission", () => {
    it("emits submit with the observation id and payload", async () => {
      const wrapper = mountComponent()

      await wrapper.find("form").trigger("submit.prevent")

      const emitted = wrapper.emitted("submit")
      expect(emitted).toBeDefined()
      expect(emitted![0][0]).toBe(42)
      const payload = emitted![0][1] as Record<string, unknown>
      expect(payload).toMatchObject({ healthStatus: "FAIR", pestPressure: "LOW" })
    })

    it("emits submit with diseaseSymptoms = true when toggled on", async () => {
      const wrapper = mountComponent()

      await wrapper.find('input[type="checkbox"]').setValue(true)
      await wrapper.find("form").trigger("submit.prevent")

      const payload = wrapper.emitted("submit")![0][1] as Record<string, unknown>
      expect(payload.diseaseSymptoms).toBe(true)
    })

    it("emits submit with updated notes", async () => {
      const wrapper = mountComponent()

      await wrapper.find("#notes").setValue("Updated observation notes")
      await wrapper.find("form").trigger("submit.prevent")

      const payload = wrapper.emitted("submit")![0][1] as Record<string, unknown>
      expect(payload.notes).toBe("Updated observation notes")
    })

    it("does not emit submit when healthStatus is invalid", async () => {
      const wrapper = mountComponent()

      const selects = wrapper.findAll('[data-stub="select"]')
      await selects[0].setValue("")
      await wrapper.find("form").trigger("submit.prevent")

      expect(wrapper.emitted("submit")).toBeUndefined()
    })

    it("shows healthStatus field error on invalid submit", async () => {
      const wrapper = mountComponent()

      const selects = wrapper.findAll('[data-stub="select"]')
      await selects[0].setValue("")
      await wrapper.find("form").trigger("submit.prevent")

      expect(wrapper.find('[data-test="healthStatusError"]').exists()).toBe(true)
    })
  })

  describe("error handling via onError callback", () => {
    it("shows field errors from API response", async () => {
      const wrapper = mountComponent()

      await wrapper.find("form").trigger("submit.prevent")

      const onError = wrapper.emitted("submit")![0][2] as (err: unknown) => void
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

      const onError = wrapper.emitted("submit")![0][2] as (err: unknown) => void
      onError(new Error("Network error"))
      await wrapper.vm.$nextTick()

      expect(wrapper.find('[data-test="general-error"]').exists()).toBe(true)
      expect(wrapper.find('[data-test="general-error"]').text()).toContain(
        "Something went wrong. Please try again.",
      )
    })
  })

  describe("loading state", () => {
    it("shows Saving... on the submit button when isLoading is true", () => {
      const wrapper = mountComponent({ isLoading: true })

      expect(wrapper.text()).toContain("Saving...")
    })
  })

  describe("close on success", () => {
    it("emits update:open false when isUpdateSuccess becomes true", async () => {
      const wrapper = mountComponent({ isUpdateSuccess: false })

      await wrapper.setProps({ isUpdateSuccess: true })

      const openEvents = wrapper.emitted("update:open")
      expect(openEvents).toBeDefined()
      expect(openEvents?.[openEvents.length - 1][0]).toBe(false)
    })
  })

  describe("form reset", () => {
    it("resets form to observationFormInitialState when dialog closes", async () => {
      const wrapper = mountComponent()

      await wrapper.find("#notes").setValue("Temporary edit")
      await wrapper.setProps({ open: false })
      await wrapper.vm.$nextTick()
      await wrapper.setProps({ open: true })
      await wrapper.vm.$nextTick()

      const notes = wrapper.find("#notes").element as HTMLTextAreaElement
      expect(notes.value).toBe("Original notes")
    })

    it("clears field errors when dialog closes", async () => {
      const wrapper = mountComponent()

      const selects = wrapper.findAll('[data-stub="select"]')
      await selects[0].setValue("")
      await wrapper.find("form").trigger("submit.prevent")
      expect(wrapper.find('[data-test="healthStatusError"]').exists()).toBe(true)

      await wrapper.setProps({ open: false })
      await wrapper.vm.$nextTick()
      await wrapper.setProps({ open: true })
      await wrapper.vm.$nextTick()

      expect(wrapper.find('[data-test="healthStatusError"]').exists()).toBe(false)
    })
  })

  describe("prop sync", () => {
    it("re-syncs form when observationFormInitialState prop changes", async () => {
      const wrapper = mountComponent()

      await wrapper.setProps({
        observationFormInitialState: {
          ...baseInitialState,
          healthStatus: "POOR",
          notes: "Updated from server",
          diseaseSymptoms: true,
        },
      })
      await wrapper.vm.$nextTick()

      const selects = wrapper.findAll('[data-stub="select"]')
      expect((selects[0].element as HTMLInputElement).value).toBe("POOR")
      const notes = wrapper.find("#notes").element as HTMLTextAreaElement
      expect(notes.value).toBe("Updated from server")
      const checkbox = wrapper.find('input[type="checkbox"]').element as HTMLInputElement
      expect(checkbox.checked).toBe(true)
    })
  })
})
