import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import CropCreateDialog from "@/components/crops/CropCreateDialog.vue"
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
  mount(CropCreateDialog, {
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

describe("CropCreateDialog.vue", () => {
  it("renders all form fields", () => {
    const wrapper = mountComponent()

    expect(wrapper.find("#name").exists()).toBe(true)
    expect(wrapper.find("#scientificName").exists()).toBe(true)
    expect(wrapper.find("#minDaysToHarvest").exists()).toBe(true)
    expect(wrapper.find("#maxDaysToHarvest").exists()).toBe(true)
    expect(wrapper.findAll('[data-stub="select"]')).toHaveLength(2)
  })

  it("shows nameError when name is empty on submit", async () => {
    const wrapper = mountComponent()

    await wrapper.find("#name").setValue("")
    await wrapper.find("form").trigger("submit.prevent")

    expect(wrapper.find('[data-test="nameError"]').exists()).toBe(true)
  })

  it("shows scientificNameError when scientificName is empty on submit", async () => {
    const wrapper = mountComponent()

    await wrapper.find("#scientificName").setValue("")
    await wrapper.find("form").trigger("submit.prevent")

    expect(wrapper.find('[data-test="scientificNameError"]').exists()).toBe(true)
  })

  it("shows minDaysToHarvestError when minDaysToHarvest is 0 on submit", async () => {
    const wrapper = mountComponent()

    await wrapper.find("#name").setValue("Tomato")
    await wrapper.find("#scientificName").setValue("Solanum lycopersicum")
    await wrapper.find("#minDaysToHarvest").setValue("0")

    await wrapper.find("form").trigger("submit.prevent")

    expect(wrapper.find('[data-test="minDaysToHarvestError"]').exists()).toBe(true)
  })

  it("shows maxDaysToHarvestError when maxDaysToHarvest is less than minDaysToHarvest on submit", async () => {
    const wrapper = mountComponent()

    await wrapper.find("#name").setValue("Tomato")
    await wrapper.find("#scientificName").setValue("Solanum lycopersicum")
    await wrapper.find("#minDaysToHarvest").setValue("80")
    await wrapper.find("#maxDaysToHarvest").setValue("60")

    await wrapper.find("form").trigger("submit.prevent")

    expect(wrapper.find('[data-test="maxDaysToHarvestError"]').exists()).toBe(true)
  })

  it("emits submit with correct payload on valid form", async () => {
    const wrapper = mountComponent()

    await wrapper.find("#name").setValue("Tomato")
    await wrapper.find("#scientificName").setValue("Solanum lycopersicum")
    await wrapper.find("#minDaysToHarvest").setValue("60")
    await wrapper.find("#maxDaysToHarvest").setValue("80")

    await wrapper.find("form").trigger("submit.prevent")

    const emitted = wrapper.emitted("submit")
    expect(emitted).toBeDefined()
    expect(emitted?.[0][0]).toMatchObject({
      name: "Tomato",
      scientificName: "Solanum lycopersicum",
      minDaysToHarvest: 60,
      maxDaysToHarvest: 80,
    })
  })

  it("shows general error when onError callback is called without response data", async () => {
    const wrapper = mountComponent()

    await wrapper.find("#name").setValue("Tomato")
    await wrapper.find("#scientificName").setValue("Solanum lycopersicum")
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
