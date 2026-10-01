import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import { today as getToday, getLocalTimeZone } from "@internationalized/date"
import FertilizerLogCreateDialog from "@/components/fertilizers/logs/FertilizerLogCreateDialog.vue"

const stubs = {
  Dialog: { template: "<div><slot /></div>" },
  DialogContent: { template: "<div><slot /></div>" },
  DialogHeader: { template: "<div><slot /></div>" },
  DialogTitle: { template: "<div><slot /></div>" },
  DialogDescription: { template: "<div><slot /></div>" },
  DialogFooter: { template: "<div><slot /></div>" },
  DialogClose: { template: "<button type='button'><slot /></button>" },
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
  Button: { template: "<button type='submit'><slot /></button>" },
  IconLoader2: { template: "<span />" },
  DatePicker: {
    template:
      '<input data-stub="date-picker" :value="modelValue" @input="$emit(\'update:modelValue\', $event.target.value)" />',
    props: ["modelValue"],
    emits: ["update:modelValue"],
  },
}

const mountComponent = (props = {}) =>
  mount(FertilizerLogCreateDialog, {
    props: {
      open: true,
      isLoading: false,
      isCreateSuccess: false,
      fertilizerName: "Swamp Fertilizer #1",
      ...props,
    },
    global: { stubs },
  })

beforeEach(() => {
  vi.clearAllMocks()
})

describe("FertilizerLogCreateDialog.vue", () => {
  describe("rendering", () => {
    it("shows the fertilizer name in the description", () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain("Swamp Fertilizer #1")
    })

    it("renders the date picker, event select, item, quantity, and notes fields", () => {
      const wrapper = mountComponent()

      expect(wrapper.find('[data-stub="date-picker"]').exists()).toBe(true)
      expect(wrapper.find('[data-stub="select"]').exists()).toBe(true)
      expect(wrapper.find("#itemAdded").exists()).toBe(true)
      expect(wrapper.find("#quantity").exists()).toBe(true)
      expect(wrapper.find("#notes").exists()).toBe(true)
    })

    it("shows Saving... on the submit button when isLoading is true", () => {
      const wrapper = mountComponent({ isLoading: true })

      expect(wrapper.text()).toContain("Saving...")
    })
  })

  describe("default form state", () => {
    it("defaults logDate to today's date", () => {
      const wrapper = mountComponent()

      const datePicker = wrapper.find('[data-stub="date-picker"]').element as HTMLInputElement
      expect(datePicker.value).toBe(getToday(getLocalTimeZone()).toString())
    })

    it("defaults eventType to OTHER", () => {
      const wrapper = mountComponent()

      const select = wrapper.find('[data-stub="select"]').element as HTMLInputElement
      expect(select.value).toBe("OTHER")
    })
  })

  describe("submission", () => {
    it("emits submit with the default payload when the form is valid", async () => {
      const today = getToday(getLocalTimeZone()).toString()
      const wrapper = mountComponent()

      await wrapper.find("form").trigger("submit.prevent")

      const emitted = wrapper.emitted("submit")
      expect(emitted).toBeDefined()
      expect(emitted![0][0]).toMatchObject({
        logDate: today,
        eventType: "OTHER",
        itemAdded: "",
        quantity: "",
        notes: "",
      })
    })

    it("emits submit with updated values", async () => {
      const wrapper = mountComponent()

      await wrapper.find('[data-stub="date-picker"]').setValue("2024-01-15")
      await wrapper.find('[data-stub="select"]').setValue("ADDED_WATER")
      await wrapper.find("#itemAdded").setValue("banana peels")
      await wrapper.find("#quantity").setValue("2 kg")
      await wrapper.find("#notes").setValue("Chopped first.")
      await wrapper.find("form").trigger("submit.prevent")

      const payload = wrapper.emitted("submit")![0][0] as Record<string, unknown>
      expect(payload).toMatchObject({
        logDate: "2024-01-15",
        eventType: "ADDED_WATER",
        itemAdded: "banana peels",
        quantity: "2 kg",
        notes: "Chopped first.",
      })
    })

    it("does not emit submit when logDate is invalid", async () => {
      const wrapper = mountComponent()

      await wrapper.find('[data-stub="date-picker"]').setValue("not-a-date")
      await wrapper.find("form").trigger("submit.prevent")

      expect(wrapper.emitted("submit")).toBeUndefined()
    })

    it("shows a field error when logDate is invalid", async () => {
      const wrapper = mountComponent()

      await wrapper.find('[data-stub="date-picker"]').setValue("not-a-date")
      await wrapper.find("form").trigger("submit.prevent")

      expect(wrapper.find('[data-test="logDateError"]').exists()).toBe(true)
    })

    it("shows a field error when eventType is invalid", async () => {
      const wrapper = mountComponent()

      await wrapper.find('[data-stub="select"]').setValue("")
      await wrapper.find("form").trigger("submit.prevent")

      expect(wrapper.find('[data-test="eventTypeError"]').exists()).toBe(true)
    })
  })

  describe("error handling via onError callback", () => {
    it("shows field errors from the API response", async () => {
      const wrapper = mountComponent()

      await wrapper.find("form").trigger("submit.prevent")

      const onError = wrapper.emitted("submit")![0][1] as (err: unknown) => void
      onError({
        response: {
          data: { message: { logDate: ["Invalid date."] } },
        },
      })
      await wrapper.vm.$nextTick()

      expect(wrapper.find('[data-test="logDateError"]').text()).toContain("Invalid date.")
    })

    it("shows a general error when the API call fails without response data", async () => {
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

  describe("form reset", () => {
    it("resets the form when the dialog is closed and reopened", async () => {
      const wrapper = mountComponent()

      await wrapper.find("#itemAdded").setValue("banana peels")
      await wrapper.setProps({ open: false })
      await wrapper.vm.$nextTick()
      await wrapper.setProps({ open: true })
      await wrapper.vm.$nextTick()

      const itemAdded = wrapper.find("#itemAdded").element as HTMLInputElement
      expect(itemAdded.value).toBe("")
    })

    it("clears field errors when the dialog is closed and reopened", async () => {
      const wrapper = mountComponent()

      await wrapper.find('[data-stub="date-picker"]').setValue("not-a-date")
      await wrapper.find("form").trigger("submit.prevent")
      expect(wrapper.find('[data-test="logDateError"]').exists()).toBe(true)

      await wrapper.setProps({ open: false })
      await wrapper.vm.$nextTick()
      await wrapper.setProps({ open: true })
      await wrapper.vm.$nextTick()

      expect(wrapper.find('[data-test="logDateError"]').exists()).toBe(false)
    })
  })
})
