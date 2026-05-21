import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import PlantingLocationSetStatusDialog from "@/components/planting-locations/status/PlantingLocationSetStatusDialog.vue"
import type { PlantingLocationStatus } from "@/types/plantingLocationStatus"

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
}

const inUseStatus: PlantingLocationStatus = {
  id: 1,
  status: "IN_USE",
  notes: "",
  image: null,
  createdAt: "2024-03-01T00:00:00Z",
}

const mountComponent = (props = {}) =>
  mount(PlantingLocationSetStatusDialog, {
    props: {
      open: true,
      currentStatus: null,
      isLoading: false,
      isCreateSuccess: false,
      ...props,
    },
    global: { stubs },
  })

beforeEach(() => {
  vi.clearAllMocks()
})

describe("PlantingLocationSetStatusDialog.vue", () => {
  describe("rendering", () => {
    it("renders form fields and Save button when location is not in use", () => {
      const wrapper = mountComponent()

      expect(wrapper.find('[data-stub="select"]').exists()).toBe(true)
      expect(wrapper.find("#notes").exists()).toBe(true)
      expect(wrapper.find("#image").exists()).toBe(true)
      expect(wrapper.findAll("button").some((b) => b.text().includes("Save"))).toBe(true)
    })

    it("renders blocked message and hides form when currentStatus is IN_USE", () => {
      const wrapper = mountComponent({ currentStatus: inUseStatus })

      expect(wrapper.find('[data-stub="select"]').exists()).toBe(false)
      expect(wrapper.find("#notes").exists()).toBe(false)
      expect(wrapper.text()).toContain("Status cannot be changed while this location is in use.")
    })

    it("hides Save button when currentStatus is IN_USE", () => {
      const wrapper = mountComponent({ currentStatus: inUseStatus })

      expect(wrapper.findAll("button").some((b) => b.text().includes("Save"))).toBe(false)
    })

    it("renders Save button when currentStatus is null", () => {
      const wrapper = mountComponent({ currentStatus: null })

      expect(wrapper.findAll("button").some((b) => b.text().includes("Save"))).toBe(true)
    })
  })

  describe("default form state", () => {
    it("status select defaults to DAMAGED", () => {
      const wrapper = mountComponent()

      const select = wrapper.find('[data-stub="select"]').element as HTMLInputElement
      expect(select.value).toBe("DAMAGED")
    })
  })

  describe("submission", () => {
    it("emits submit with payload on valid submit", async () => {
      const wrapper = mountComponent()

      await wrapper.find("#notes").setValue("Some notes.")
      await wrapper.find("form").trigger("submit.prevent")

      const emitted = wrapper.emitted("submit")
      expect(emitted).toBeDefined()
      expect(emitted![0][0]).toEqual({ status: "DAMAGED", notes: "Some notes." })
    })

    it("emits submit with selected status", async () => {
      const wrapper = mountComponent()

      await wrapper.find('[data-stub="select"]').setValue("RETIRED")
      await wrapper.find("form").trigger("submit.prevent")

      const emitted = wrapper.emitted("submit")
      expect(emitted![0][0]).toMatchObject({ status: "RETIRED" })
    })

    it("emits submit with image when a file is selected", async () => {
      const wrapper = mountComponent()

      const file = new File(["content"], "photo.jpg", { type: "image/jpeg" })
      const input = wrapper.find("#image").element as HTMLInputElement
      Object.defineProperty(input, "files", { value: [file], configurable: true })
      await wrapper.find("#image").trigger("change")
      await wrapper.find("form").trigger("submit.prevent")

      const emitted = wrapper.emitted("submit")
      expect(emitted![0][0]).toMatchObject({ image: file })
    })

    it("does not emit submit when form is invalid", async () => {
      // Force a Zod validation error by using an invalid status value
      const wrapper = mountComponent()

      await wrapper.find('[data-stub="select"]').setValue("INVALID_STATUS")
      await wrapper.find("form").trigger("submit.prevent")

      expect(wrapper.emitted("submit")).toBeUndefined()
    })
  })

  describe("error handling", () => {
    it("calls onError callback and shows general error on network failure", async () => {
      const wrapper = mountComponent()

      await wrapper.find("form").trigger("submit.prevent")

      const emitted = wrapper.emitted("submit")!
      const onError = emitted[0][1] as (err: unknown) => void
      onError(new Error("Network error"))
      await wrapper.vm.$nextTick()

      expect(wrapper.find('[data-test="general-error"]').exists()).toBe(true)
      expect(wrapper.find('[data-test="general-error"]').text()).toContain(
        "Something went wrong. Please try again.",
      )
    })

    it("shows field errors when onError receives an axios response error", async () => {
      const wrapper = mountComponent()

      await wrapper.find("form").trigger("submit.prevent")

      const { AxiosError } = await import("axios")
      const error = new AxiosError("Bad request")
      error.response = {
        data: { message: { status: ["Invalid choice."] } },
        status: 400,
        statusText: "Bad Request",
        headers: {},
        config: {} as never,
      }

      const onError = wrapper.emitted("submit")![0][1] as (err: unknown) => void
      onError(error)
      await wrapper.vm.$nextTick()

      expect(wrapper.find('[data-test="statusError"]').exists()).toBe(true)
    })
  })

  describe("loading state", () => {
    it("shows Saving... text when isLoading is true", () => {
      const wrapper = mountComponent({ isLoading: true })

      expect(wrapper.findAll("button").some((b) => b.text().includes("Saving..."))).toBe(true)
    })
  })

  describe("form reset", () => {
    it("resets notes when dialog is closed", async () => {
      const wrapper = mountComponent()

      await wrapper.find("#notes").setValue("Some notes.")
      await wrapper.setProps({ open: false })
      await wrapper.vm.$nextTick()
      await wrapper.setProps({ open: true })
      await wrapper.vm.$nextTick()

      const notes = wrapper.find("#notes").element as HTMLTextAreaElement
      expect(notes.value).toBe("")
    })
  })

  describe("close on success", () => {
    it("emits update:open false when isCreateSuccess becomes true", async () => {
      const wrapper = mountComponent()

      await wrapper.setProps({ isCreateSuccess: true })
      await wrapper.vm.$nextTick()

      const openEvents = wrapper.emitted("update:open")
      expect(openEvents).toBeDefined()
      expect(openEvents?.[openEvents.length - 1][0]).toBe(false)
    })
  })
})
