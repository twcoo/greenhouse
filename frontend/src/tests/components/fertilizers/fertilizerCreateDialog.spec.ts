import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import FertilizerCreateDialog from "@/components/fertilizers/FertilizerCreateDialog.vue"
import { createTestingPinia } from "@pinia/testing"

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
  DatePicker: {
    template:
      '<input data-stub="datepicker" :value="modelValue" @input="$emit(\'update:modelValue\', $event.target.value)" />',
    props: ["modelValue"],
    emits: ["update:modelValue"],
  },
  IconLoader2: { template: "<svg />" },
  IconPlus: { template: "<svg />" },
  IconX: { template: "<svg />" },
}

const mountComponent = (props = {}) =>
  mount(FertilizerCreateDialog, {
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

describe("FertilizerCreateDialog.vue", () => {
  it("renders name input and ingredient input", () => {
    const wrapper = mountComponent()

    expect(wrapper.find("#name").exists()).toBe(true)
    expect(wrapper.find("#ingredientInput").exists()).toBe(true)
  })

  it("shows validation error when name is empty on submit", async () => {
    const wrapper = mountComponent()

    await wrapper.find("#name").setValue("")
    await wrapper.find("form").trigger("submit.prevent")

    expect(wrapper.find('[data-test="nameError"]').exists()).toBe(true)
  })

  it("adds an ingredient via Enter key and renders a chip", async () => {
    const wrapper = mountComponent()

    const input = wrapper.find("#ingredientInput")
    await input.setValue("banana peels")
    await input.trigger("keydown.enter")

    expect(wrapper.text()).toContain("banana peels")
  })

  it("does not add duplicate ingredients", async () => {
    const wrapper = mountComponent()

    const input = wrapper.find("#ingredientInput")
    await input.setValue("banana peels")
    await input.trigger("keydown.enter")
    await input.setValue("banana peels")
    await input.trigger("keydown.enter")

    const chips = wrapper.findAll('[data-test="remove-ingredient"]')
    expect(chips).toHaveLength(1)
  })

  it("removes an ingredient when the chip remove button is clicked", async () => {
    const wrapper = mountComponent()

    const input = wrapper.find("#ingredientInput")
    await input.setValue("banana peels")
    await input.trigger("keydown.enter")

    await wrapper.find('[data-test="remove-ingredient"]').trigger("click")

    expect(wrapper.text()).not.toContain("banana peels")
  })

  it("emits submit with valid payload on submit", async () => {
    const wrapper = mountComponent()

    await wrapper.find("#name").setValue("Swamp Fertilizer #1")
    await wrapper.find("form").trigger("submit.prevent")

    const emitted = wrapper.emitted("submit")
    expect(emitted).toBeDefined()
    expect(emitted?.[0][0]).toMatchObject({
      name: "Swamp Fertilizer #1",
      type: "SWAMP",
      status: "BREWING",
    })
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
