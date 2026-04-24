import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import PlantingCreateDialog from "@/components/plantings/PlantingCreateDialog.vue"
import { createTestingPinia } from "@pinia/testing"

vi.mock("@/composables/useCrops", () => ({
  useCrop: vi.fn(() => ({
    crops: { value: { results: [{ id: 1, name: "Tomato" }], count: 1 } },
  })),
}))

vi.mock("@/composables/useVarieties", () => ({
  useVarieties: vi.fn(() => ({
    varieties: {
      value: { results: [{ id: 1, name: "Sun Gold", crop: 1 }], count: 1 },
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
  Button: { template: "<button type='submit'><slot /></button>" },
  IconLoader2: { template: "<svg />" },
}

const mountComponent = (props = {}) =>
  mount(PlantingCreateDialog, {
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

describe("PlantingCreateDialog.vue", () => {
  it("renders crop and variety selects", () => {
    const wrapper = mountComponent()
    expect(wrapper.findAll('[data-stub="select"]').length).toBe(2)
  })

  it("shows cropError when form is submitted with no crop selected", async () => {
    const wrapper = mountComponent()

    await wrapper.find("form").trigger("submit.prevent")

    expect(wrapper.find('[data-test="cropError"]').exists()).toBe(true)
  })

  it("shows varietyError when form is submitted with no variety selected", async () => {
    const wrapper = mountComponent()

    // Select a crop but leave variety empty
    const selects = wrapper.findAll('[data-stub="select"]')
    await selects[0].setValue("1")
    await wrapper.find("form").trigger("submit.prevent")

    expect(wrapper.find('[data-test="varietyError"]').exists()).toBe(true)
  })

  it("emits submit with correct payload on valid form", async () => {
    const wrapper = mountComponent()

    const selects = wrapper.findAll('[data-stub="select"]')
    await selects[0].setValue("1")
    await selects[1].setValue("1")
    await wrapper.find("form").trigger("submit.prevent")

    const emitted = wrapper.emitted("submit")
    expect(emitted).toBeDefined()
    expect(emitted?.[0][0]).toMatchObject({ crop: 1, variety: 1 })
  })

  it("shows general error when onError callback is called without response data", async () => {
    const wrapper = mountComponent()

    const selects = wrapper.findAll('[data-stub="select"]')
    await selects[0].setValue("1")
    await selects[1].setValue("1")
    await wrapper.find("form").trigger("submit.prevent")

    const emitted = wrapper.emitted("submit")
    const onError = emitted?.[0][1] as (err: unknown) => void
    onError(new Error("Network error"))
    await wrapper.vm.$nextTick()

    expect(wrapper.find('[data-test="general-error"]').exists()).toBe(true)
  })

  it("shows loading text on button when isLoading is true", () => {
    const wrapper = mountComponent({ isLoading: true })
    expect(wrapper.text()).toContain("Saving")
  })

  it("emits update:open with false when isCreateSuccess becomes true", async () => {
    const wrapper = mountComponent({ isCreateSuccess: false })

    await wrapper.setProps({ isCreateSuccess: true })

    const openEvents = wrapper.emitted("update:open")
    expect(openEvents).toBeDefined()
    expect(openEvents?.[openEvents.length - 1][0]).toBe(false)
  })
})
