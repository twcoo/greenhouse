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
  wateringEvent: null,
  fertilizerType: "NONE",
  fertilizerDetail: "",
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
  describe("health section", () => {
    it("always shows the Health section header", () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain("Health")
    })

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

    it("shows disease row with 'Present' text when diseaseSymptoms is true", () => {
      const wrapper = mountComponent({ ...baseObservation, diseaseSymptoms: true })

      expect(wrapper.text()).toContain("Disease")
      expect(wrapper.text()).toContain("Present")
    })

    it("hides disease row when diseaseSymptoms is false", () => {
      const wrapper = mountComponent({ ...baseObservation, diseaseSymptoms: false })

      expect(wrapper.text()).not.toContain("Present")
    })
  })

  describe("watering section", () => {
    it("shows the Watering section header when wateringEvent is set", () => {
      const wrapper = mountComponent({ ...baseObservation, wateringEvent: "WATERED" })

      expect(wrapper.text()).toContain("Watering")
    })

    it("shows Watered badge when wateringEvent is WATERED", () => {
      const wrapper = mountComponent({ ...baseObservation, wateringEvent: "WATERED" })

      expect(wrapper.text()).toContain("Watered")
    })

    it("shows Rained badge when wateringEvent is RAINED", () => {
      const wrapper = mountComponent({ ...baseObservation, wateringEvent: "RAINED" })

      expect(wrapper.text()).toContain("Rained (skipped watering)")
    })

    it("shows Soil still wet badge when wateringEvent is SKIPPED_WET", () => {
      const wrapper = mountComponent({ ...baseObservation, wateringEvent: "SKIPPED_WET" })

      expect(wrapper.text()).toContain("Soil still wet (skipped watering)")
    })

    it("hides the Watering section when wateringEvent is null", () => {
      const wrapper = mountComponent({ ...baseObservation, wateringEvent: null })

      expect(wrapper.text()).not.toContain("Watering")
    })
  })

  describe("pruning section", () => {
    it("shows the Pruning section header when pruned is true", () => {
      const wrapper = mountComponent({ ...baseObservation, pruned: true })

      expect(wrapper.text()).toContain("Pruning")
    })

    it("shows 'Yes' when pruned is true and no detail is present", () => {
      const wrapper = mountComponent({ ...baseObservation, pruned: true, pruningDetail: "" })

      expect(wrapper.text()).toContain("Yes")
    })

    it("shows pruning detail text when pruned is true and detail is present", () => {
      const wrapper = mountComponent({
        ...baseObservation,
        pruned: true,
        pruningDetail: "removed lower leaves",
      })

      expect(wrapper.text()).toContain("removed lower leaves")
    })

    it("shows the Detail label when pruned is true and detail is present", () => {
      const wrapper = mountComponent({
        ...baseObservation,
        pruned: true,
        pruningDetail: "removed lower leaves",
      })

      expect(wrapper.text()).toContain("Detail")
    })

    it("hides the Pruning section when pruned is false", () => {
      const wrapper = mountComponent({ ...baseObservation, pruned: false })

      expect(wrapper.text()).not.toContain("Pruning")
    })

    it("hides pruning detail when pruned is false even if pruningDetail has a value", () => {
      const wrapper = mountComponent({
        ...baseObservation,
        pruned: false,
        pruningDetail: "removed lower leaves",
      })

      expect(wrapper.text()).not.toContain("removed lower leaves")
    })
  })

  describe("fertilization section", () => {
    it("shows the Fertilization section header when fertilizerType is not NONE", () => {
      const wrapper = mountComponent({ ...baseObservation, fertilizerType: "ORGANIC" })

      expect(wrapper.text()).toContain("Fertilization")
    })

    it("shows Organic badge when fertilizerType is ORGANIC", () => {
      const wrapper = mountComponent({ ...baseObservation, fertilizerType: "ORGANIC" })

      expect(wrapper.text()).toContain("Organic")
    })

    it("shows Synthetic badge when fertilizerType is SYNTHETIC", () => {
      const wrapper = mountComponent({ ...baseObservation, fertilizerType: "SYNTHETIC" })

      expect(wrapper.text()).toContain("Synthetic")
    })

    it("hides the Fertilization section when fertilizerType is NONE", () => {
      const wrapper = mountComponent({ ...baseObservation, fertilizerType: "NONE" })

      expect(wrapper.text()).not.toContain("Fertilization")
    })

    it("shows fertilizer detail when type is not NONE and detail is present", () => {
      const wrapper = mountComponent({
        ...baseObservation,
        fertilizerType: "ORGANIC",
        fertilizerDetail: "fermented swamp fertilizer",
      })

      expect(wrapper.text()).toContain("fermented swamp fertilizer")
    })

    it("hides fertilizer detail text when fertilizerDetail is empty", () => {
      const wrapper = mountComponent({
        ...baseObservation,
        fertilizerType: "ORGANIC",
        fertilizerDetail: "",
      })

      // Only the section Type row renders — no detail value text present
      expect(wrapper.text()).not.toContain("fermented swamp fertilizer")
    })
  })

  describe("notes section", () => {
    it("displays notes when present", () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain("Healthy today")
    })

    it("hides the notes section when notes is empty", () => {
      const wrapper = mountComponent({ ...baseObservation, notes: "" })

      expect(wrapper.text()).not.toContain("Notes")
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

      expect(wrapper.text()).toMatch(/Mar.*2024|2024.*Mar/)
    })

    it("renders a different observationDate when provided", () => {
      const wrapper = mountComponent({ ...baseObservation, observationDate: "2023-07-04" })

      expect(wrapper.text()).toMatch(/Jul.*2023|2023.*Jul/)
    })
  })
})
