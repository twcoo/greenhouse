import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import PlantingLocationCreateDialog from "@/components/planting-locations/PlantingLocationCreateDialog.vue"
import { createTestingPinia } from "@pinia/testing"

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

const mountComponent = (props = {}) =>
  mount(PlantingLocationCreateDialog, {
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

describe("PlantingLocationCreateDialog.vue", () => {
  it("renders core form fields for POT type (default)", () => {
    const wrapper = mountComponent()

    expect(wrapper.find("#name").exists()).toBe(true)
    expect(wrapper.find("#width").exists()).toBe(true)
    expect(wrapper.find("#height").exists()).toBe(true)
    expect(wrapper.find("#length").exists()).toBe(false)
  })

  it("shows length field and hides height field when GROUND type is selected", async () => {
    const wrapper = mountComponent()

    await wrapper.find('[data-stub="select"]').setValue("GROUND")
    await wrapper.vm.$nextTick()

    expect(wrapper.find("#length").exists()).toBe(true)
    expect(wrapper.find("#height").exists()).toBe(false)
  })

  it("shows validation error when name is empty on submit", async () => {
    const wrapper = mountComponent()

    await wrapper.find("#name").setValue("")
    await wrapper.find("form").trigger("submit.prevent")

    expect(wrapper.find('[data-test="name"]').exists()).toBe(true)
  })

  it("emits submit event with validated payload on valid form", async () => {
    const wrapper = mountComponent()

    await wrapper.find("#name").setValue("My Pot")
    await wrapper.find("#width").setValue("20")
    await wrapper.find("#height").setValue("30")

    await wrapper.find("form").trigger("submit.prevent")

    const emitted = wrapper.emitted("submit")
    expect(emitted).toBeDefined()
    expect(emitted?.[0][0]).toMatchObject({
      name: "My Pot",
      locationType: "POT",
      width: 20,
      height: 30,
    })
  })

  it("shows general error when API error callback is triggered without response data", async () => {
    const wrapper = mountComponent()

    await wrapper.find("#name").setValue("My Pot")
    await wrapper.find("#width").setValue("20")
    await wrapper.find("#height").setValue("30")

    await wrapper.find("form").trigger("submit.prevent")

    const emitted = wrapper.emitted("submit")
    expect(emitted).toBeDefined()

    const onError = emitted?.[0][1] as (err: unknown) => void
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

  it("closes dialog and emits update:open false when isCreateSuccess becomes true", async () => {
    const wrapper = mountComponent({ isCreateSuccess: false })

    await wrapper.setProps({ isCreateSuccess: true })

    const openEvents = wrapper.emitted("update:open")
    expect(openEvents).toBeDefined()
    expect(openEvents?.[openEvents.length - 1][0]).toBe(false)
  })
})
