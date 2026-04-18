import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import VarietyCreateDialog from "@/components/varieties/VarietyCreateDialog.vue"
import { createTestingPinia } from "@pinia/testing"

vi.mock("@/composables/useCrops", () => ({
  useCrop: vi.fn(() => ({
    crops: { value: { results: [{ id: 1, name: "Tomato" }], count: 1 } },
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

const mountComponent = (props = {}) =>
  mount(VarietyCreateDialog, {
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

describe("VarietyCreateDialog.vue", () => {
  it("renders name input, crop select, and growth habit checkboxes", () => {
    const wrapper = mountComponent()

    expect(wrapper.find("#name").exists()).toBe(true)
    expect(wrapper.find('[data-stub="select"]').exists()).toBe(true)
    expect(wrapper.find("#create-determinate").exists()).toBe(true)
    expect(wrapper.find("#create-indeterminate").exists()).toBe(true)
  })

  it("shows validation error when name is empty on submit", async () => {
    const wrapper = mountComponent()

    await wrapper.find("#name").setValue("")
    await wrapper.find("form").trigger("submit.prevent")

    expect(wrapper.find('[data-test="nameError"]').exists()).toBe(true)
  })

  it("shows validation error when no crop is selected on submit", async () => {
    const wrapper = mountComponent()

    await wrapper.find("#name").setValue("Sun Gold")
    await wrapper.find("form").trigger("submit.prevent")

    expect(wrapper.find('[data-test="cropError"]').exists()).toBe(true)
  })

  it("shows validation error when no growth habit is checked on submit", async () => {
    const wrapper = mountComponent()

    await wrapper.find("#name").setValue("Sun Gold")
    await wrapper.find('[data-stub="select"]').setValue("1")
    // uncheck the default DETERMINATE selection by setting the DOM state then firing change
    const determinateCheckbox = wrapper.find("#create-determinate")
    ;(determinateCheckbox.element as HTMLInputElement).checked = false
    await determinateCheckbox.trigger("change")

    await wrapper.find("form").trigger("submit.prevent")

    expect(wrapper.find('[data-test="growthHabitError"]').exists()).toBe(true)
  })

  it("emits submit with correct payload on valid form", async () => {
    const wrapper = mountComponent()

    await wrapper.find("#name").setValue("Sun Gold")
    await wrapper.find('[data-stub="select"]').setValue("1")
    const determinateCheckbox = wrapper.find(
      "#create-determinate",
    ).element as HTMLInputElement
    if (!determinateCheckbox.checked) {
      await wrapper
        .find("#create-determinate")
        .trigger("change", { target: { checked: true } })
    }

    await wrapper.find("form").trigger("submit.prevent")

    const emitted = wrapper.emitted("submit")
    expect(emitted).toBeDefined()
    expect(emitted?.[0][0]).toMatchObject({
      name: "Sun Gold",
      crop: 1,
    })
  })

  it("shows general error when onError callback is called without response data", async () => {
    const wrapper = mountComponent()

    await wrapper.find("#name").setValue("Sun Gold")
    await wrapper.find('[data-stub="select"]').setValue("1")
    await wrapper.find("form").trigger("submit.prevent")

    const emitted = wrapper.emitted("submit")
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

  it("closes dialog when isCreateSuccess becomes true", async () => {
    const wrapper = mountComponent({ isCreateSuccess: false })

    await wrapper.setProps({ isCreateSuccess: true })

    const openEvents = wrapper.emitted("update:open")
    expect(openEvents).toBeDefined()
    expect(openEvents?.[openEvents.length - 1][0]).toBe(false)
  })
})
