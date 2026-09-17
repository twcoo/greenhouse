import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import FertilizerUpdateDialog from "@/components/fertilizers/FertilizerUpdateDialog.vue"
import { createTestingPinia } from "@pinia/testing"
import type { fertilizerForm } from "@/schemas/fertilizer.schemas"

const initialState: fertilizerForm = {
  name: "Swamp Fertilizer #1",
  type: "SWAMP",
  status: "BREWING",
  startDate: "2024-01-01",
  ingredients: ["banana peels"],
  notes: "Fermenting.",
}

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
  mount(FertilizerUpdateDialog, {
    props: {
      open: true,
      id: 1,
      fertilizerFormInitialState: initialState,
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

describe("FertilizerUpdateDialog.vue", () => {
  it("pre-populates the name and ingredients from initial state", () => {
    const wrapper = mountComponent()

    expect((wrapper.find("#name").element as HTMLInputElement).value).toBe("Swamp Fertilizer #1")
    expect(wrapper.text()).toContain("banana peels")
  })

  it("shows validation error when name is emptied on submit", async () => {
    const wrapper = mountComponent()

    await wrapper.find("#name").setValue("")
    await wrapper.find("form").trigger("submit.prevent")

    expect(wrapper.find('[data-test="nameError"]').exists()).toBe(true)
  })

  it("emits submit with id and payload on submit", async () => {
    const wrapper = mountComponent()

    await wrapper.find("#name").setValue("Updated Fertilizer")
    await wrapper.find("form").trigger("submit.prevent")

    const emitted = wrapper.emitted("submit")
    expect(emitted).toBeDefined()
    expect(emitted?.[0][0]).toBe(1)
    expect(emitted?.[0][1]).toMatchObject({ name: "Updated Fertilizer" })
  })

  it("closes dialog when isUpdateSuccess becomes true", async () => {
    const wrapper = mountComponent({ isUpdateSuccess: false })

    await wrapper.setProps({ isUpdateSuccess: true })

    const openEvents = wrapper.emitted("update:open")
    expect(openEvents).toBeDefined()
    expect(openEvents?.[openEvents.length - 1][0]).toBe(false)
  })
})
