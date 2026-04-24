import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import PlantingUpdateDialog from "@/components/plantings/PlantingUpdateDialog.vue"
import { createTestingPinia } from "@pinia/testing"
import type { plantingForm } from "@/schemas/planting.schemas"

vi.mock("@/composables/useCrops", () => ({
  useCrop: vi.fn(() => ({
    crops: { value: { results: [{ id: 1, name: "Tomato" }], count: 1 } },
  })),
}))

vi.mock("@/composables/useVarieties", () => ({
  useVarieties: vi.fn(() => ({
    varieties: {
      value: {
        results: [
          { id: 1, name: "Sun Gold", crop: 1 },
          { id: 2, name: "Cherokee Purple", crop: 1 },
        ],
        count: 2,
      },
    },
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
  FieldGroup: { template: "<div><slot /></div>" },
  Field: { template: "<div><slot /></div>" },
  FieldLabel: { template: "<label><slot /></label>" },
  FieldError: { template: "<p v-bind='$attrs'><slot /></p>" },
  Button: {
    template: "<button type='submit' v-bind='$attrs'><slot /></button>",
    inheritAttrs: false,
  },
  IconLoader2: { template: "<svg />" },
}

const defaultInitialState: plantingForm = {
  crop: 1,
  variety: 1,
}

const mountComponent = (props = {}) =>
  mount(PlantingUpdateDialog, {
    props: {
      open: true,
      id: 1,
      plantingFormInitialState: defaultInitialState,
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

describe("PlantingUpdateDialog.vue", () => {
  it("pre-populates crop and variety selects from initial state", () => {
    const wrapper = mountComponent()

    const selects = wrapper.findAll('[data-stub="select"]')
    expect((selects[0].element as HTMLInputElement).value).toBe("1")
    expect((selects[1].element as HTMLInputElement).value).toBe("1")
  })

  it("emits submit with id and validated payload on valid form", async () => {
    const wrapper = mountComponent()

    const selects = wrapper.findAll('[data-stub="select"]')
    await selects[1].setValue("2")
    await wrapper.find("form").trigger("submit.prevent")

    const emitted = wrapper.emitted("submit")
    expect(emitted).toBeDefined()
    expect(emitted?.[0][0]).toBe(1)
    expect(emitted?.[0][1]).toMatchObject({ crop: 1, variety: 2 })
  })

  it("emits update:open with false when isUpdateSuccess becomes true", async () => {
    const wrapper = mountComponent({ isUpdateSuccess: false })

    await wrapper.setProps({ isUpdateSuccess: true })

    const openEvents = wrapper.emitted("update:open")
    expect(openEvents).toBeDefined()
    expect(openEvents?.[openEvents.length - 1][0]).toBe(false)
  })

  it("shows loading text and disables save button when isLoading is true", () => {
    const wrapper = mountComponent({ isLoading: true })
    expect(wrapper.text()).toContain("Saving")
  })

  it("shows general error when onError is called without response data", async () => {
    const wrapper = mountComponent()

    await wrapper.find("form").trigger("submit.prevent")

    const emitted = wrapper.emitted("submit")
    const onError = emitted?.[0][2] as (err: unknown) => void
    onError(new Error("Network error"))
    await wrapper.vm.$nextTick()

    expect(wrapper.find('[data-test="general-error"]').exists()).toBe(true)
  })

  it("clears errors when dialog is closed", async () => {
    const wrapper = mountComponent()

    // Trigger a validation error
    const selects = wrapper.findAll('[data-stub="select"]')
    await selects[0].setValue("")
    await wrapper.find("form").trigger("submit.prevent")
    expect(wrapper.find('[data-test="cropError"]').exists()).toBe(true)

    await wrapper.setProps({ open: false })
    await wrapper.vm.$nextTick()
    await wrapper.setProps({ open: true })
    await wrapper.vm.$nextTick()

    expect(wrapper.find('[data-test="cropError"]').exists()).toBe(false)
  })

  it("syncs form values when plantingFormInitialState prop changes", async () => {
    const wrapper = mountComponent()

    const newState: plantingForm = { crop: 1, variety: 2 }
    await wrapper.setProps({ plantingFormInitialState: newState })
    await wrapper.vm.$nextTick()

    const selects = wrapper.findAll('[data-stub="select"]')
    expect((selects[1].element as HTMLInputElement).value).toBe("2")
  })
})
