import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import PlantingLocationUpdateDialog from "@/components/planting-locations/PlantingLocationUpdateDialog.vue"
import { createTestingPinia } from "@pinia/testing"
import type { PlantingLocationForm } from "@/schemas/plantingLocation.schemas"

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

const defaultInitialState: PlantingLocationForm = {
  name: "Garden Pot",
  locationType: "POT",
  width: 25,
  height: 35,
  length: undefined,
}

const mountComponent = (props = {}) =>
  mount(PlantingLocationUpdateDialog, {
    props: {
      open: true,
      id: 1,
      locationFormInitialState: defaultInitialState,
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

describe("PlantingLocationUpdateDialog.vue", () => {
  it("pre-populates the form with initial state", () => {
    const wrapper = mountComponent()

    const nameInput = wrapper.find("#name").element as HTMLInputElement
    expect(nameInput.value).toBe("Garden Pot")

    const widthInput = wrapper.find("#width").element as HTMLInputElement
    expect(Number(widthInput.value)).toBe(25)
  })

  it("emits submit with id and validated payload on valid form", async () => {
    const wrapper = mountComponent()

    await wrapper.find("#name").setValue("Updated Pot")
    await wrapper.find("form").trigger("submit.prevent")

    const emitted = wrapper.emitted("submit")
    expect(emitted).toBeDefined()
    expect(emitted?.[0][0]).toBe(1)
    expect(emitted?.[0][1]).toMatchObject({
      name: "Updated Pot",
      locationType: "POT",
      width: 25,
      height: 35,
    })
  })

  it("disables the submit button when isLoading is true", () => {
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

    // Trigger a validation error
    await wrapper.find("#name").setValue("")
    await wrapper.find("form").trigger("submit.prevent")
    expect(wrapper.find('[data-test="name"]').exists()).toBe(true)

    // Close the dialog
    await wrapper.setProps({ open: false })
    await wrapper.vm.$nextTick()

    // Reopen
    await wrapper.setProps({ open: true })
    await wrapper.vm.$nextTick()

    expect(wrapper.find('[data-test="name"]').exists()).toBe(false)
  })

  it("updates form when locationFormInitialState prop changes", async () => {
    const wrapper = mountComponent()

    const newState: PlantingLocationForm = {
      name: "New Ground Bed",
      locationType: "GROUND",
      width: 100,
      height: undefined,
      length: 200,
    }
    await wrapper.setProps({ locationFormInitialState: newState })
    await wrapper.vm.$nextTick()

    const nameInput = wrapper.find("#name").element as HTMLInputElement
    expect(nameInput.value).toBe("New Ground Bed")
  })
})
