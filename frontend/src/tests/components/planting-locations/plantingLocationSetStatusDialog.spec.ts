import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import { ref } from "vue"
import PlantingLocationSetStatusDialog from "@/components/planting-locations/status/PlantingLocationSetStatusDialog.vue"
import type { PlantingLocationStatus } from "@/types/plantingLocationStatus"
import { AxiosError } from "axios"

const mockCreateStatus = vi.fn()
const mockIsLoading = ref(false)
const mockIsCreateSuccess = ref(false)

vi.mock("@/composables/usePlantingLocationStatuses", () => ({
  usePlantingLocationStatuses: vi.fn(() => ({
    statuses: ref(null),
    isLoading: mockIsLoading,
    isQueryError: ref(false),
    createError: ref(false),
    isCreateSuccess: mockIsCreateSuccess,
    createStatus: mockCreateStatus,
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
      locationId: 1,
      currentStatus: null,
      ...props,
    },
    global: { stubs },
  })

beforeEach(() => {
  vi.clearAllMocks()
  mockIsLoading.value = false
  mockIsCreateSuccess.value = false
  mockCreateStatus.mockResolvedValue(undefined)
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
    it("calls createStatus with correct id and payload on valid submit", async () => {
      const wrapper = mountComponent()

      await wrapper.find("#notes").setValue("Some notes.")
      await wrapper.find("form").trigger("submit.prevent")

      expect(mockCreateStatus).toHaveBeenCalledWith({
        id: 1,
        payload: { status: "DAMAGED", notes: "Some notes." },
      })
    })

    it("calls createStatus with selected status", async () => {
      const wrapper = mountComponent()

      await wrapper.find('[data-stub="select"]').setValue("RETIRED")
      await wrapper.find("form").trigger("submit.prevent")

      expect(mockCreateStatus).toHaveBeenCalledWith({
        id: 1,
        payload: expect.objectContaining({ status: "RETIRED" }),
      })
    })

    it("calls createStatus with image when a file is selected", async () => {
      const wrapper = mountComponent()

      const file = new File(["content"], "photo.jpg", { type: "image/jpeg" })
      const input = wrapper.find("#image").element as HTMLInputElement
      Object.defineProperty(input, "files", { value: [file], configurable: true })
      await wrapper.find("#image").trigger("change")
      await wrapper.find("form").trigger("submit.prevent")

      expect(mockCreateStatus).toHaveBeenCalledWith({
        id: 1,
        payload: expect.objectContaining({ image: file }),
      })
    })

    it("does not call createStatus when locationId is null", async () => {
      const wrapper = mountComponent({ locationId: null })

      await wrapper.find("form").trigger("submit.prevent")

      expect(mockCreateStatus).not.toHaveBeenCalled()
    })
  })

  describe("loading state", () => {
    it("shows Saving... text when isLoading is true", () => {
      mockIsLoading.value = true
      const wrapper = mountComponent()

      const buttons = wrapper.findAll("button")
      expect(buttons.some((b) => b.text().includes("Saving..."))).toBe(true)
    })
  })

  describe("error handling", () => {
    it("shows general error when createStatus throws without response data", async () => {
      mockCreateStatus.mockRejectedValue(new AxiosError("Network error"))
      const wrapper = mountComponent()

      await wrapper.find("form").trigger("submit.prevent")
      await wrapper.vm.$nextTick()

      expect(wrapper.find('[data-test="general-error"]').exists()).toBe(true)
      expect(wrapper.find('[data-test="general-error"]').text()).toContain(
        "Something went wrong. Please try again.",
      )
    })

    it("shows field errors when createStatus throws with response data", async () => {
      const error = new AxiosError("Bad request")
      error.response = {
        data: { message: { status: ["Invalid choice."] } },
        status: 400,
        statusText: "Bad Request",
        headers: {},
        config: {} as never,
      }
      mockCreateStatus.mockRejectedValue(error)
      const wrapper = mountComponent()

      await wrapper.find("form").trigger("submit.prevent")
      await wrapper.vm.$nextTick()

      expect(wrapper.find('[data-test="statusError"]').exists()).toBe(true)
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

      mockIsCreateSuccess.value = true
      await wrapper.vm.$nextTick()

      const openEvents = wrapper.emitted("update:open")
      expect(openEvents).toBeDefined()
      expect(openEvents?.[openEvents.length - 1][0]).toBe(false)
    })
  })
})
