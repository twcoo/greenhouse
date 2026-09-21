import { mount } from "@vue/test-utils"
import { describe, it, expect } from "vitest"
import FertilizerLogViewDialog from "@/components/fertilizers/logs/FertilizerLogViewDialog.vue"
import type { FertilizerLog, FertilizerLogEventType } from "@/types/fertilizerLog"

const stubs = {
  Dialog: { template: "<div><slot /></div>" },
  DialogContent: { template: "<div><slot /></div>" },
  DialogHeader: { template: "<div><slot /></div>" },
  DialogTitle: { template: "<div><slot /></div>" },
  DialogDescription: { template: "<div><slot /></div>" },
  Badge: { template: "<span data-test='badge'><slot /></span>" },
}

const baseLog: FertilizerLog = {
  id: 1,
  eventType: "ADDED_INGREDIENT",
  itemAdded: "banana peels",
  quantity: "2 kg",
  notes: "Chopped first.",
  logDate: "2024-03-01",
  createdAt: "2024-03-01T00:00:00Z",
  updatedAt: "2024-03-01T00:00:00Z",
}

const mountComponent = (log: FertilizerLog | null = baseLog) =>
  mount(FertilizerLogViewDialog, {
    props: { open: true, log },
    global: { stubs },
  })

describe("FertilizerLogViewDialog.vue", () => {
  describe("event type", () => {
    it("shows the mapped label for a known event type", () => {
      const wrapper = mountComponent()

      expect(wrapper.find('[data-test="badge"]').text()).toBe("Added Ingredient")
    })

    it("falls back to the raw event type when no label is mapped", () => {
      const wrapper = mountComponent({
        ...baseLog,
        eventType: "UNKNOWN_EVENT" as FertilizerLogEventType,
      })

      expect(wrapper.find('[data-test="badge"]').text()).toBe("UNKNOWN_EVENT")
    })
  })

  describe("item added", () => {
    it("shows the item added when present", () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain("Item Added")
      expect(wrapper.text()).toContain("banana peels")
    })

    it("hides the item added when empty", () => {
      const wrapper = mountComponent({ ...baseLog, itemAdded: "" })

      expect(wrapper.text()).not.toContain("Item Added")
    })
  })

  describe("quantity", () => {
    it("shows the quantity when present", () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain("Quantity")
      expect(wrapper.text()).toContain("2 kg")
    })

    it("hides the quantity when empty", () => {
      const wrapper = mountComponent({ ...baseLog, quantity: "" })

      expect(wrapper.text()).not.toContain("Quantity")
    })
  })

  describe("notes", () => {
    it("shows the notes when present", () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain("Notes")
      expect(wrapper.text()).toContain("Chopped first.")
    })

    it("hides the notes when empty", () => {
      const wrapper = mountComponent({ ...baseLog, notes: "" })

      expect(wrapper.text()).not.toContain("Notes")
    })
  })

  describe("date and empty state", () => {
    it("renders the log date in the description", () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toMatch(/Mar.*2024|2024.*Mar/)
    })

    it("renders no details when log is null", () => {
      const wrapper = mountComponent(null)

      expect(wrapper.text()).not.toContain("Item Added")
      expect(wrapper.text()).not.toContain("Notes")
    })
  })
})
