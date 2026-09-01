import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import { today as getToday, getLocalTimeZone } from "@internationalized/date"
import PlantingDailyObservationCreateDialog from "@/components/plantings/daily-observation/PlantingDailyObservationCreateDialog.vue"

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
  IconX: { template: "<span />" },
  DatePicker: {
    template:
      '<input data-stub="date-picker" :value="modelValue" @input="$emit(\'update:modelValue\', $event.target.value)" />',
    props: ["modelValue"],
    emits: ["update:modelValue"],
  },
}

const mountComponent = (props = {}) =>
  mount(PlantingDailyObservationCreateDialog, {
    props: {
      open: true,
      isLoading: false,
      isCreateSuccess: false,
      ...props,
    },
    global: { stubs },
  })

beforeEach(() => {
  vi.clearAllMocks()
})

describe("PlantingDailyObservationCreateDialog.vue", () => {
  describe("rendering", () => {
    it("renders the observation date picker", () => {
      const wrapper = mountComponent()

      expect(wrapper.find('[data-stub="date-picker"]').exists()).toBe(true)
    })

    it("renders health status, pest pressure, watering event, and fertilizer type selects", () => {
      const wrapper = mountComponent()

      const selects = wrapper.findAll('[data-stub="select"]')
      expect(selects).toHaveLength(4)
    })

    it("renders the disease symptoms checkbox", () => {
      const wrapper = mountComponent()

      expect(wrapper.find('input[type="checkbox"]').exists()).toBe(true)
    })

    it("renders the disease symptoms and pruned checkboxes", () => {
      const wrapper = mountComponent()

      expect(wrapper.findAll('input[type="checkbox"]')).toHaveLength(2)
    })

    it("renders the notes textarea", () => {
      const wrapper = mountComponent()

      expect(wrapper.find("#notes").exists()).toBe(true)
    })

    it("renders the image input area", () => {
      const wrapper = mountComponent()

      expect(wrapper.find('[data-test="image-input-area"]').exists()).toBe(true)
    })

    it("shows Saving... on the submit button when isLoading is true", () => {
      const wrapper = mountComponent({ isLoading: true })

      expect(wrapper.text()).toContain("Saving...")
    })
  })

  describe("default form state", () => {
    it("defaults observationDate to today's date", () => {
      const today = getToday(getLocalTimeZone()).toString()
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

    it("defaults diseaseSymptoms checkbox to unchecked", () => {
      const wrapper = mountComponent()

      const checkbox = wrapper.findAll('input[type="checkbox"]')[0].element as HTMLInputElement
      expect(checkbox.checked).toBe(false)
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

    it("does not render fertilizerDetail input when fertilizerType is NONE", () => {
      const wrapper = mountComponent()

      expect(wrapper.find("#fertilizerDetail").exists()).toBe(false)
    })

    it("renders fertilizerDetail input when fertilizerType is changed to ORGANIC", async () => {
      const wrapper = mountComponent()

      await wrapper.findAll('[data-stub="select"]')[3].setValue("ORGANIC")

      expect(wrapper.find("#fertilizerDetail").exists()).toBe(true)
    })

    it("does not render pruningDetail input when pruned is unchecked", () => {
      const wrapper = mountComponent()

      expect(wrapper.find("#pruningDetail").exists()).toBe(false)
    })

    it("renders pruningDetail input when pruned checkbox is checked", async () => {
      const wrapper = mountComponent()

      await wrapper.findAll('input[type="checkbox"]')[1].setValue(true)

      expect(wrapper.find("#pruningDetail").exists()).toBe(true)
    })
  })

  describe("submission", () => {
    it("emits submit with default payload when form is valid", async () => {
      const today = getToday(getLocalTimeZone()).toString()
      const wrapper = mountComponent()

      await wrapper.find("form").trigger("submit.prevent")

      const emitted = wrapper.emitted("submit")
      expect(emitted).toBeDefined()
      const payload = emitted![0][0] as Record<string, unknown>
      expect(payload).toMatchObject({
        observationDate: today,
        healthStatus: "GOOD",
        pestPressure: "NONE",
        diseaseSymptoms: false,
        fertilizerType: "NONE",
        pruned: false,
      })
      expect(payload.wateringEvent).toBeUndefined()
    })

    it("emits submit with updated observationDate when date picker changes", async () => {
      const wrapper = mountComponent()

      await wrapper.find('[data-stub="date-picker"]').setValue("2024-01-15")
      await wrapper.find("form").trigger("submit.prevent")

      const payload = wrapper.emitted("submit")![0][0] as Record<string, unknown>
      expect(payload.observationDate).toBe("2024-01-15")
    })

    it("emits submit with updated healthStatus when changed", async () => {
      const wrapper = mountComponent()

      const selects = wrapper.findAll('[data-stub="select"]')
      await selects[0].setValue("POOR")
      await wrapper.find("form").trigger("submit.prevent")

      const payload = wrapper.emitted("submit")![0][0] as Record<string, unknown>
      expect(payload.healthStatus).toBe("POOR")
    })

    it("emits submit with diseaseSymptoms = true when checkbox is checked", async () => {
      const wrapper = mountComponent()

      await wrapper.findAll('input[type="checkbox"]')[0].setValue(true)
      await wrapper.find("form").trigger("submit.prevent")

      const payload = wrapper.emitted("submit")![0][0] as Record<string, unknown>
      expect(payload.diseaseSymptoms).toBe(true)
    })

    it("emits submit with wateringEvent WATERED when changed", async () => {
      const wrapper = mountComponent()

      await wrapper.findAll('[data-stub="select"]')[2].setValue("WATERED")
      await wrapper.find("form").trigger("submit.prevent")

      const payload = wrapper.emitted("submit")![0][0] as Record<string, unknown>
      expect(payload.wateringEvent).toBe("WATERED")
    })

    it("emits submit with pruned = true when pruned checkbox is checked", async () => {
      const wrapper = mountComponent()

      await wrapper.findAll('input[type="checkbox"]')[1].setValue(true)
      await wrapper.find("form").trigger("submit.prevent")

      const payload = wrapper.emitted("submit")![0][0] as Record<string, unknown>
      expect(payload.pruned).toBe(true)
    })

    it("emits submit with notes when provided", async () => {
      const wrapper = mountComponent()

      await wrapper.find("#notes").setValue("Looking great today")
      await wrapper.find("form").trigger("submit.prevent")

      const payload = wrapper.emitted("submit")![0][0] as Record<string, unknown>
      expect(payload.notes).toBe("Looking great today")
    })

    it("emits submit with pruningDetail when pruned and detail provided", async () => {
      const wrapper = mountComponent()

      await wrapper.findAll('input[type="checkbox"]')[1].setValue(true)
      await wrapper.find("#pruningDetail").setValue("removed lower leaves")
      await wrapper.find("form").trigger("submit.prevent")

      const payload = wrapper.emitted("submit")![0][0] as Record<string, unknown>
      expect(payload.pruned).toBe(true)
      expect(payload.pruningDetail).toBe("removed lower leaves")
    })

    it("emits submit with image when a file is selected", async () => {
      const wrapper = mountComponent()

      const file = new File(["content"], "photo.jpg", { type: "image/jpeg" })
      const input = wrapper.find('input[type="file"]').element as HTMLInputElement
      Object.defineProperty(input, "files", { value: [file], configurable: true })
      await wrapper.find('input[type="file"]').trigger("change")
      await wrapper.find("form").trigger("submit.prevent")

      const payload = wrapper.emitted("submit")![0][0] as Record<string, unknown>
      expect(payload.image).toBe(file)
    })

    it("emits submit with fertilizerType ORGANIC when changed", async () => {
      const wrapper = mountComponent()

      await wrapper.findAll('[data-stub="select"]')[3].setValue("ORGANIC")
      await wrapper.find("form").trigger("submit.prevent")

      const payload = wrapper.emitted("submit")![0][0] as Record<string, unknown>
      expect(payload.fertilizerType).toBe("ORGANIC")
    })

    it("emits submit with fertilizerDetail when provided", async () => {
      const wrapper = mountComponent()

      await wrapper.findAll('[data-stub="select"]')[3].setValue("ORGANIC")
      await wrapper.find("#fertilizerDetail").setValue("fermented swamp fertilizer")
      await wrapper.find("form").trigger("submit.prevent")

      const payload = wrapper.emitted("submit")![0][0] as Record<string, unknown>
      expect(payload.fertilizerDetail).toBe("fermented swamp fertilizer")
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

      expect(wrapper.find('[data-test="general-error"]').exists()).toBe(true)
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

  describe("image management", () => {
    it("shows 'No image' when no file is selected", () => {
      const wrapper = mountComponent()

      expect(wrapper.find('[data-test="image-input-area"]').text()).toContain("No image")
    })

    it("remove button is not visible when no file is selected", () => {
      const wrapper = mountComponent()

      expect(wrapper.find('[data-test="remove-image-button"]').exists()).toBe(false)
    })

    it("shows filename in input area after file is selected", async () => {
      const wrapper = mountComponent()

      const file = new File(["content"], "photo.jpg", { type: "image/jpeg" })
      const input = wrapper.find('input[type="file"]').element as HTMLInputElement
      Object.defineProperty(input, "files", { value: [file], configurable: true })
      await wrapper.find('input[type="file"]').trigger("change")

      expect(wrapper.find('[data-test="image-input-area"]').text()).toContain("photo.jpg")
    })

    it("shows remove button after file is selected", async () => {
      const wrapper = mountComponent()

      const file = new File(["content"], "photo.jpg", { type: "image/jpeg" })
      const input = wrapper.find('input[type="file"]').element as HTMLInputElement
      Object.defineProperty(input, "files", { value: [file], configurable: true })
      await wrapper.find('input[type="file"]').trigger("change")

      expect(wrapper.find('[data-test="remove-image-button"]').exists()).toBe(true)
    })

    it("clears file and shows 'No image' after remove button is clicked", async () => {
      const wrapper = mountComponent()

      const file = new File(["content"], "photo.jpg", { type: "image/jpeg" })
      const input = wrapper.find('input[type="file"]').element as HTMLInputElement
      Object.defineProperty(input, "files", { value: [file], configurable: true })
      await wrapper.find('input[type="file"]').trigger("change")
      await wrapper.find('[data-test="remove-image-button"]').trigger("click")

      expect(wrapper.find('[data-test="image-input-area"]').text()).toContain("No image")
      expect(wrapper.find('[data-test="remove-image-button"]').exists()).toBe(false)
    })

    it("emits submit with image: undefined after file is removed", async () => {
      const wrapper = mountComponent()

      const file = new File(["content"], "photo.jpg", { type: "image/jpeg" })
      const input = wrapper.find('input[type="file"]').element as HTMLInputElement
      Object.defineProperty(input, "files", { value: [file], configurable: true })
      await wrapper.find('input[type="file"]').trigger("change")
      await wrapper.find('[data-test="remove-image-button"]').trigger("click")
      await wrapper.find("form").trigger("submit.prevent")

      const payload = wrapper.emitted("submit")![0][0] as Record<string, unknown>
      expect(payload.image).toBeUndefined()
    })

    it("resets image state when dialog reopens", async () => {
      const wrapper = mountComponent()

      const file = new File(["content"], "photo.jpg", { type: "image/jpeg" })
      const input = wrapper.find('input[type="file"]').element as HTMLInputElement
      Object.defineProperty(input, "files", { value: [file], configurable: true })
      await wrapper.find('input[type="file"]').trigger("change")
      expect(wrapper.find('[data-test="image-input-area"]').text()).toContain("photo.jpg")

      await wrapper.setProps({ open: false })
      await wrapper.vm.$nextTick()
      await wrapper.setProps({ open: true })
      await wrapper.vm.$nextTick()

      expect(wrapper.find('[data-test="image-input-area"]').text()).toContain("No image")
      expect(wrapper.find('[data-test="remove-image-button"]').exists()).toBe(false)
    })
  })

  describe("form reset", () => {
    it("resets observationDate to today when dialog is closed and reopened", async () => {
      const today = getToday(getLocalTimeZone()).toString()
      const wrapper = mountComponent()

      await wrapper.find('[data-stub="date-picker"]').setValue("2020-01-01")
      await wrapper.setProps({ open: false })
      await wrapper.vm.$nextTick()
      await wrapper.setProps({ open: true })
      await wrapper.vm.$nextTick()

      const datePicker = wrapper.find('[data-stub="date-picker"]').element as HTMLInputElement
      expect(datePicker.value).toBe(today)
    })

    it("resets notes when dialog is closed", async () => {
      const wrapper = mountComponent()

      await wrapper.find("#notes").setValue("Some observation notes")
      await wrapper.setProps({ open: false })
      await wrapper.vm.$nextTick()
      await wrapper.setProps({ open: true })
      await wrapper.vm.$nextTick()

      const notes = wrapper.find("#notes").element as HTMLTextAreaElement
      expect(notes.value).toBe("")
    })

    it("clears field errors when dialog is closed", async () => {
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

    it("resets pruningDetail when dialog is closed and reopened", async () => {
      const wrapper = mountComponent()

      await wrapper.findAll('input[type="checkbox"]')[1].setValue(true)
      await wrapper.find("#pruningDetail").setValue("removed lower leaves")

      await wrapper.setProps({ open: false })
      await wrapper.vm.$nextTick()
      await wrapper.setProps({ open: true })
      await wrapper.vm.$nextTick()

      // pruned resets to false — check it to reveal pruningDetail and confirm it's empty
      await wrapper.findAll('input[type="checkbox"]')[1].setValue(true)
      const pruningDetailInput = wrapper.find("#pruningDetail").element as HTMLInputElement
      expect(pruningDetailInput.value).toBe("")
    })
  })
})
