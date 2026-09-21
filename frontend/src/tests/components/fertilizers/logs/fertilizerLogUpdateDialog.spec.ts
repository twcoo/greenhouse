import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import FertilizerLogUpdateDialog from "@/components/fertilizers/logs/FertilizerLogUpdateDialog.vue"
import type { FertilizerLogForm } from "@/schemas/fertilizerLog.schemas"

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

const baseInitialState: FertilizerLogForm = {
  logDate: "2024-03-10",
  eventType: "ADDED_INGREDIENT",
  itemAdded: "banana peels",
  quantity: "2 kg",
  notes: "Original notes",
}

const mountComponent = (props = {}) =>
  mount(FertilizerLogUpdateDialog, {
    props: {
      open: true,
      id: 42,
      logFormInitialState: baseInitialState,
      isLoading: false,
      isUpdateSuccess: false,
      ...props,
    },
    global: { stubs },
  })

beforeEach(() => {
  vi.clearAllMocks()
})

describe("FertilizerLogUpdateDialog.vue", () => {
  describe("form pre-population", () => {
    it("pre-populates logDate from logFormInitialState", () => {
      const wrapper = mountComponent()

      const datePicker = wrapper.find('[data-stub="date-picker"]').element as HTMLInputElement
      expect(datePicker.value).toBe("2024-03-10")
    })

    it("pre-populates eventType from logFormInitialState", () => {
      const wrapper = mountComponent()

      const select = wrapper.find('[data-stub="select"]').element as HTMLInputElement
      expect(select.value).toBe("ADDED_INGREDIENT")
    })

    it("pre-populates itemAdded, quantity, and notes from logFormInitialState", () => {
      const wrapper = mountComponent()

      expect((wrapper.find("#itemAdded").element as HTMLInputElement).value).toBe("banana peels")
      expect((wrapper.find("#quantity").element as HTMLInputElement).value).toBe("2 kg")
      expect((wrapper.find("#notes").element as HTMLTextAreaElement).value).toBe("Original notes")
    })

    it("shows Saving... on the submit button when isLoading is true", () => {
      const wrapper = mountComponent({ isLoading: true })

      expect(wrapper.text()).toContain("Saving...")
    })
  })

  describe("submission", () => {
    it("emits submit with the id and payload", async () => {
      const wrapper = mountComponent()

      await wrapper.find("form").trigger("submit.prevent")

      const emitted = wrapper.emitted("submit")
      expect(emitted).toBeDefined()
      expect(emitted![0][0]).toBe(42)
      expect(emitted![0][1]).toMatchObject({
        logDate: "2024-03-10",
        eventType: "ADDED_INGREDIENT",
        itemAdded: "banana peels",
        quantity: "2 kg",
        notes: "Original notes",
      })
    })

    it("emits submit with updated values", async () => {
      const wrapper = mountComponent()

      await wrapper.find('[data-stub="date-picker"]').setValue("2024-04-01")
      await wrapper.find('[data-stub="select"]').setValue("STIRRED")
      await wrapper.find("#itemAdded").setValue("")
      await wrapper.find("#quantity").setValue("3 kg")
      await wrapper.find("#notes").setValue("Stirred well.")
      await wrapper.find("form").trigger("submit.prevent")

      const payload = wrapper.emitted("submit")![0][1] as Record<string, unknown>
      expect(payload).toMatchObject({
        logDate: "2024-04-01",
        eventType: "STIRRED",
        itemAdded: "",
        quantity: "3 kg",
        notes: "Stirred well.",
      })
    })

    it("does not emit submit when logDate is invalid", async () => {
      const wrapper = mountComponent()

      await wrapper.find('[data-stub="date-picker"]').setValue("not-a-date")
      await wrapper.find("form").trigger("submit.prevent")

      expect(wrapper.emitted("submit")).toBeUndefined()
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

      const onError = wrapper.emitted("submit")![0][2] as (err: unknown) => void
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

      const onError = wrapper.emitted("submit")![0][2] as (err: unknown) => void
      onError(new Error("Network error"))
      await wrapper.vm.$nextTick()

      expect(wrapper.find('[data-test="general-error"]').exists()).toBe(true)
      expect(wrapper.find('[data-test="general-error"]').text()).toContain(
        "Something went wrong. Please try again.",
      )
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

  describe("form sync and reset", () => {
    it("re-syncs the form when logFormInitialState changes", async () => {
      const wrapper = mountComponent()

      await wrapper.setProps({
        logFormInitialState: {
          ...baseInitialState,
          logDate: "2024-05-05",
          eventType: "ADDED_WATER",
          quantity: "10 liters",
          notes: "Updated from server",
        },
      })
      await wrapper.vm.$nextTick()

      expect((wrapper.find('[data-stub="date-picker"]').element as HTMLInputElement).value).toBe(
        "2024-05-05",
      )
      expect((wrapper.find("#quantity").element as HTMLInputElement).value).toBe("10 liters")
      expect((wrapper.find("#notes").element as HTMLTextAreaElement).value).toBe(
        "Updated from server",
      )
    })

    it("resets the form to logFormInitialState when the dialog is closed and reopened", async () => {
      const wrapper = mountComponent()

      await wrapper.find("#notes").setValue("Temporary edit")
      await wrapper.setProps({ open: false })
      await wrapper.vm.$nextTick()
      await wrapper.setProps({ open: true })
      await wrapper.vm.$nextTick()

      expect((wrapper.find("#notes").element as HTMLTextAreaElement).value).toBe("Original notes")
    })
  })
})
