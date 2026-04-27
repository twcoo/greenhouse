import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import DatePicker from "@/components/DatePicker.vue"

const stubs = {
  Popover: { template: "<div><slot /></div>" },
  PopoverTrigger: { template: "<div><slot /></div>" },
  PopoverContent: { template: "<div><slot /></div>" },
  Button: { template: "<button :disabled='disabled'><slot /></button>", props: ["disabled"] },
  IconCalendar: { template: "<span />" },
  Calendar: {
    name: "Calendar",
    template: "<div />",
    props: ["modelValue"],
    emits: ["update:modelValue"],
  },
}

const mountComponent = (props = {}) =>
  mount(DatePicker, {
    props,
    global: { stubs },
  })

beforeEach(() => {
  vi.clearAllMocks()
})

describe("DatePicker.vue", () => {
  it("shows placeholder text when no modelValue is set", () => {
    const wrapper = mountComponent({ placeholder: "Pick a start date" })

    expect(wrapper.text()).toContain("Pick a start date")
  })

  it("falls back to 'Pick a date' when no placeholder or modelValue is provided", () => {
    const wrapper = mountComponent()

    expect(wrapper.text()).toContain("Pick a date")
  })

  it("displays the formatted date when a valid modelValue is set", () => {
    const wrapper = mountComponent({ modelValue: "2024-03-15" })

    expect(wrapper.text()).toContain("March 15, 2024")
  })

  it("falls back to placeholder when modelValue is an invalid date string", () => {
    const wrapper = mountComponent({ modelValue: "not-a-date", placeholder: "Pick a date" })

    expect(wrapper.text()).toContain("Pick a date")
  })

  it("disables the trigger button when disabled prop is true", () => {
    const wrapper = mountComponent({ disabled: true })

    const button = wrapper.find("button")
    expect(button.attributes("disabled")).toBeDefined()
  })

  it("does not disable the trigger button when disabled prop is false", () => {
    const wrapper = mountComponent({ disabled: false })

    const button = wrapper.find("button")
    expect(button.attributes("disabled")).toBeUndefined()
  })

  it("emits update:modelValue with the ISO string when Calendar selects a date", async () => {
    const wrapper = mountComponent({ modelValue: "2024-03-01" })

    const { parseDate } = await import("@internationalized/date")
    const selected = parseDate("2024-06-15")

    await wrapper.findComponent({ name: "Calendar" }).vm.$emit("update:modelValue", selected)

    const emitted = wrapper.emitted("update:modelValue")
    expect(emitted).toBeDefined()
    expect(emitted?.[0][0]).toBe("2024-06-15")
  })

  it("emits update:modelValue with undefined when Calendar clears the selection", async () => {
    const wrapper = mountComponent({ modelValue: "2024-03-01" })

    await wrapper.findComponent({ name: "Calendar" }).vm.$emit("update:modelValue", undefined)

    const emitted = wrapper.emitted("update:modelValue")
    expect(emitted?.[0][0]).toBeUndefined()
  })
})
