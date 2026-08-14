import { mount } from "@vue/test-utils"
import { describe, it, expect } from "vitest"
import PlantingDailyObservationViewDialog from "@/components/plantings/daily-observation/PlantingDailyObservationViewDialog.vue"
import type { PlantingDailyObservation } from "@/types/plantingDailyObservation"

const stubs = {
  Dialog: { template: "<div><slot /></div>" },
  DialogContent: { template: "<div><slot /></div>" },
  DialogHeader: { template: "<div><slot /></div>" },
  DialogTitle: { template: "<div><slot /></div>" },
  DialogDescription: { template: "<div><slot /></div>" },
  Badge: { template: "<span data-test='badge'><slot /></span>" },
}

const baseObservation: PlantingDailyObservation = {
  id: 1,
  stage: null,
  stageName: null,
  healthStatus: "GOOD",
  pestPressure: "LOW",
  diseaseSymptoms: false,
  watered: false,
  rained: false,
  pruned: false,
  pruningDetail: "",
  notes: "Healthy today",
  image: null,
  observationDate: "2024-03-01",
  createdAt: "2024-03-01T00:00:00Z",
  updatedAt: "2024-03-01T00:00:00Z",
}

const mountComponent = (observation: PlantingDailyObservation | null = baseObservation) =>
  mount(PlantingDailyObservationViewDialog, {
    props: { open: true, observation },
    global: { stubs },
  })

describe("PlantingDailyObservationViewDialog.vue", () => {
  describe("health and pest status", () => {
    it("shows the health label for GOOD status", () => {
      const wrapper = mountComponent()

      expect(wrapper.find('[data-test="badge"]').text()).toBe("Good")
    })

    it("shows the health label for POOR status", () => {
      const wrapper = mountComponent({ ...baseObservation, healthStatus: "POOR" })

      expect(wrapper.find('[data-test="badge"]').text()).toBe("Poor")
    })

    it("shows the pest pressure label", () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain("Low")
    })
  })

  describe("disease symptoms", () => {
    it("shows disease symptoms text when diseaseSymptoms is true", () => {
      const wrapper = mountComponent({ ...baseObservation, diseaseSymptoms: true })

      expect(wrapper.text()).toContain("Disease symptoms present")
    })

    it("hides disease symptoms text when diseaseSymptoms is false", () => {
      const wrapper = mountComponent({ ...baseObservation, diseaseSymptoms: false })

      expect(wrapper.text()).not.toContain("Disease symptoms present")
    })
  })

  describe("watered", () => {
    it("shows Watered badge when watered is true", () => {
      const wrapper = mountComponent({ ...baseObservation, watered: true })

      expect(wrapper.text()).toContain("Watered")
    })

    it("hides Watered badge when watered is false", () => {
      const wrapper = mountComponent({ ...baseObservation, watered: false })

      const badges = wrapper.findAll('[data-test="badge"]')
      expect(badges.every((b) => b.text() !== "Watered")).toBe(true)
    })
  })

  describe("rained", () => {
    it("shows Rained badge when rained is true", () => {
      const wrapper = mountComponent({ ...baseObservation, rained: true })

      expect(wrapper.text()).toContain("Rained")
    })

    it("hides Rained badge when rained is false", () => {
      const wrapper = mountComponent({ ...baseObservation, rained: false })

      const badges = wrapper.findAll('[data-test="badge"]')
      expect(badges.every((b) => b.text() !== "Rained")).toBe(true)
    })
  })

  describe("pruned", () => {
    it("shows Pruned badge when pruned is true", () => {
      const wrapper = mountComponent({ ...baseObservation, pruned: true })

      expect(wrapper.text()).toContain("Pruned")
    })

    it("hides Pruned badge when pruned is false", () => {
      const wrapper = mountComponent({ ...baseObservation, pruned: false })

      const badges = wrapper.findAll('[data-test="badge"]')
      expect(badges.every((b) => b.text() !== "Pruned")).toBe(true)
    })

    it("shows pruning detail when pruned is true and detail is present", () => {
      const wrapper = mountComponent({
        ...baseObservation,
        pruned: true,
        pruningDetail: "removed lower leaves",
      })

      expect(wrapper.text()).toContain("removed lower leaves")
    })

    it("hides pruning detail section when pruned is false", () => {
      const wrapper = mountComponent({
        ...baseObservation,
        pruned: false,
        pruningDetail: "removed lower leaves",
      })

      expect(wrapper.text()).not.toContain("Pruning detail")
    })

    it("hides pruning detail section when pruned is true but detail is empty", () => {
      const wrapper = mountComponent({
        ...baseObservation,
        pruned: true,
        pruningDetail: "",
      })

      expect(wrapper.text()).not.toContain("Pruning detail")
    })
  })

  describe("notes", () => {
    it("displays notes when present", () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain("Healthy today")
    })

    it("does not render the notes section when notes is empty", () => {
      const wrapper = mountComponent({ ...baseObservation, notes: "" })

      expect(wrapper.text()).not.toContain("Healthy today")
    })
  })

  describe("image", () => {
    it("renders observation image when an image URL is present", () => {
      const wrapper = mountComponent({
        ...baseObservation,
        image: "https://example.com/photo.jpg",
      })

      const img = wrapper.find('img[alt="Observation image"]')
      expect(img.exists()).toBe(true)
      expect(img.attributes("src")).toBe("https://example.com/photo.jpg")
    })

    it("hides observation image when image is null", () => {
      const wrapper = mountComponent({ ...baseObservation, image: null })

      expect(wrapper.find('img[alt="Observation image"]').exists()).toBe(false)
    })
  })

  describe("date", () => {
    it("renders the observationDate in the description", () => {
      const wrapper = mountComponent()

      // formatDate("2024-03-01") → "Mar 1, 2024" (or similar)
      expect(wrapper.text()).toMatch(/Mar.*2024|2024.*Mar/)
    })

    it("renders a different observationDate when provided", () => {
      const wrapper = mountComponent({ ...baseObservation, observationDate: "2023-07-04" })

      expect(wrapper.text()).toMatch(/Jul.*2023|2023.*Jul/)
    })
  })
})
