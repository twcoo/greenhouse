import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import VarietyUpdateDialog from "@/components/varieties/VarietyUpdateDialog.vue"
import { createTestingPinia } from "@pinia/testing"
import type { varietyForm } from "@/schemas/variety.schemas"

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

const defaultInitialState: varietyForm = {
  name: "Sun Gold",
  crop: 1,
  growthHabit: ["INDETERMINATE"],
}

const mountComponent = (props = {}) =>
  mount(VarietyUpdateDialog, {
    props: {
      open: true,
      id: 1,
      varietyFormInitialState: defaultInitialState,
      isLoading: false,
      isUpdateSuccess: false,
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

describe("VarietyUpdateDialog.vue", () => {
  it("pre-populates the form with initial state", () => {
    const wrapper = mountComponent()

    const nameInput = wrapper.find("#name").element as HTMLInputElement
    expect(nameInput.value).toBe("Sun Gold")
  })

  it("emits submit with id and validated payload on valid form", async () => {
    const wrapper = mountComponent()

    await wrapper.find("#name").setValue("Cherokee Purple")
    await wrapper.find("form").trigger("submit.prevent")

    const emitted = wrapper.emitted("submit")
    expect(emitted).toBeDefined()
    expect(emitted?.[0][0]).toBe(1)
    expect(emitted?.[0][1]).toMatchObject({
      name: "Cherokee Purple",
      crop: 1,
    })
  })

  it("shows validation error when name is cleared before submit", async () => {
    const wrapper = mountComponent()

    await wrapper.find("#name").setValue("")
    await wrapper.find("form").trigger("submit.prevent")

    expect(wrapper.find('[data-test="nameError"]').exists()).toBe(true)
  })

  it("disables submit button and shows loading text when isLoading is true", () => {
    const wrapper = mountComponent({ isLoading: true })

    const buttons = wrapper.findAll("button")
    const saveButton = buttons.find((b) => b.text().includes("Saving"))
    expect(saveButton).toBeDefined()
    expect(saveButton?.attributes("disabled")).toBeDefined()
  })

  it("closes dialog when isUpdateSuccess becomes true", async () => {
    const wrapper = mountComponent({ isUpdateSuccess: false })

    await wrapper.setProps({ isUpdateSuccess: true })

    const openEvents = wrapper.emitted("update:open")
    expect(openEvents).toBeDefined()
    expect(openEvents?.[openEvents.length - 1][0]).toBe(false)
  })

  it("clears errors when dialog is closed and reopened", async () => {
    const wrapper = mountComponent()

    await wrapper.find("#name").setValue("")
    await wrapper.find("form").trigger("submit.prevent")
    expect(wrapper.find('[data-test="nameError"]').exists()).toBe(true)

    await wrapper.setProps({ open: false })
    await wrapper.vm.$nextTick()

    await wrapper.setProps({ open: true })
    await wrapper.vm.$nextTick()

    expect(wrapper.find('[data-test="nameError"]').exists()).toBe(false)
  })

  it("syncs form when varietyFormInitialState prop changes", async () => {
    const wrapper = mountComponent()

    const newState: varietyForm = {
      name: "Black Krim",
      crop: 2,
      growthHabit: ["DETERMINATE"],
    }
    await wrapper.setProps({ varietyFormInitialState: newState })
    await wrapper.vm.$nextTick()

    const nameInput = wrapper.find("#name").element as HTMLInputElement
    expect(nameInput.value).toBe("Black Krim")
  })
})
