import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import CropUpdateDialog from "@/components/crops/CropUpdateDialog.vue"
import { createTestingPinia } from "@pinia/testing"
import type { cropsForm } from "@/schemas/crops.schemas"

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

const defaultInitialState: cropsForm = {
  name: "Tomato",
  scientificName: "Solanum lycopersicum",
  category: "VEGETABLE",
  sunlightRequirement: "FULL SUN",
  minDaysToHarvest: 60,
  maxDaysToHarvest: 80,
}

const mountComponent = (props = {}) =>
  mount(CropUpdateDialog, {
    props: {
      open: true,
      id: 1,
      cropsFormInitialState: defaultInitialState,
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

describe("CropUpdateDialog.vue", () => {
  it("pre-populates the form with initial state", () => {
    const wrapper = mountComponent()

    const nameInput = wrapper.find("#name").element as HTMLInputElement
    expect(nameInput.value).toBe("Tomato")

    const scientificNameInput = wrapper.find("#scientificName").element as HTMLInputElement
    expect(scientificNameInput.value).toBe("Solanum lycopersicum")
  })

  it("emits submit with id and validated payload on valid form", async () => {
    const wrapper = mountComponent()

    await wrapper.find("#name").setValue("Cherry Tomato")
    await wrapper.find("form").trigger("submit.prevent")

    const emitted = wrapper.emitted("submit")
    expect(emitted).toBeDefined()
    expect(emitted?.[0][0]).toBe(1)
    expect(emitted?.[0][1]).toMatchObject({
      name: "Cherry Tomato",
      scientificName: "Solanum lycopersicum",
    })
  })

  it("shows nameError when name is cleared before submit", async () => {
    const wrapper = mountComponent()

    await wrapper.find("#name").setValue("")
    await wrapper.find("form").trigger("submit.prevent")

    expect(wrapper.find('[data-test="nameError"]').exists()).toBe(true)
  })

  it("shows scientificNameError when scientificName is cleared before submit", async () => {
    const wrapper = mountComponent()

    await wrapper.find("#scientificName").setValue("")
    await wrapper.find("form").trigger("submit.prevent")

    expect(wrapper.find('[data-test="scientificNameError"]').exists()).toBe(true)
  })

  it("shows minDaysToHarvestError when minDaysToHarvest is 0 before submit", async () => {
    const wrapper = mountComponent()

    await wrapper.find("#minDaysToHarvest").setValue("0")
    await wrapper.find("form").trigger("submit.prevent")

    expect(wrapper.find('[data-test="minDaysToHarvestError"]').exists()).toBe(true)
  })

  it("shows maxDaysToHarvestError when maxDaysToHarvest is less than minDaysToHarvest before submit", async () => {
    const wrapper = mountComponent()

    await wrapper.find("#minDaysToHarvest").setValue("80")
    await wrapper.find("#maxDaysToHarvest").setValue("60")
    await wrapper.find("form").trigger("submit.prevent")

    expect(wrapper.find('[data-test="maxDaysToHarvestError"]').exists()).toBe(true)
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

  it("syncs form when cropsFormInitialState prop changes", async () => {
    const wrapper = mountComponent()

    const newState: cropsForm = {
      name: "Pepper",
      scientificName: "Capsicum annuum",
      category: "VEGETABLE",
      sunlightRequirement: "FULL SUN",
      minDaysToHarvest: 70,
      maxDaysToHarvest: 90,
    }
    await wrapper.setProps({ cropsFormInitialState: newState })
    await wrapper.vm.$nextTick()

    const nameInput = wrapper.find("#name").element as HTMLInputElement
    expect(nameInput.value).toBe("Pepper")
  })
})
