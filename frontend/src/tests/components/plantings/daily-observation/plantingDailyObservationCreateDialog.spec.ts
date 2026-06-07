import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
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
    it("renders health status and pest pressure selects", () => {
      const wrapper = mountComponent()

      const selects = wrapper.findAll('[data-stub="select"]')
      expect(selects).toHaveLength(2)
    })

    it("renders the disease symptoms checkbox", () => {
      const wrapper = mountComponent()

      expect(wrapper.find('input[type="checkbox"]').exists()).toBe(true)
    })

    it("renders the watered checkbox", () => {
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

    it("defaults watered checkbox to unchecked", () => {
      const wrapper = mountComponent()

      const checkbox = wrapper.findAll('input[type="checkbox"]')[1].element as HTMLInputElement
      expect(checkbox.checked).toBe(false)
    })
  })

  describe("submission", () => {
    it("emits submit with default payload when form is valid", async () => {
      const wrapper = mountComponent()

      await wrapper.find("form").trigger("submit.prevent")

      const emitted = wrapper.emitted("submit")
      expect(emitted).toBeDefined()
      const payload = emitted![0][0] as Record<string, unknown>
      expect(payload).toMatchObject({
        healthStatus: "GOOD",
        pestPressure: "NONE",
        diseaseSymptoms: false,
        watered: false,
      })
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

    it("emits submit with watered = true when watered checkbox is checked", async () => {
      const wrapper = mountComponent()

      await wrapper.findAll('input[type="checkbox"]')[1].setValue(true)
      await wrapper.find("form").trigger("submit.prevent")

      const payload = wrapper.emitted("submit")![0][0] as Record<string, unknown>
      expect(payload.watered).toBe(true)
    })

    it("emits submit with notes when provided", async () => {
      const wrapper = mountComponent()

      await wrapper.find("#notes").setValue("Looking great today")
      await wrapper.find("form").trigger("submit.prevent")

      const payload = wrapper.emitted("submit")![0][0] as Record<string, unknown>
      expect(payload.notes).toBe("Looking great today")
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
  })
})
