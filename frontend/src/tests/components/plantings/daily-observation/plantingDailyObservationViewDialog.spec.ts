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
  heightCm: "15.50",
  leafCount: 3,
  temperatureC: "22.0",
  humidityPercent: "65.0",
  lightHours: "8.0",
  soilMoisturePercent: "40.0",
  soilPh: "6.5",
  ecMsCm: "1.2",
  notes: "Healthy today",
  image: null,
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

  describe("measurement fields", () => {
    it("displays heightCm value", () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain("15.50")
    })

    it("displays — when heightCm is null", () => {
      const wrapper = mountComponent({ ...baseObservation, heightCm: null })

      expect(wrapper.text()).toContain("—")
    })

    it("displays leafCount value", () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain("3")
    })

    it("displays — when leafCount is null", () => {
      const wrapper = mountComponent({ ...baseObservation, leafCount: null })

      const text = wrapper.text()
      expect(text).toContain("—")
    })

    it("displays temperatureC value", () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain("22.0")
    })

    it("displays — when temperatureC is null", () => {
      const wrapper = mountComponent({ ...baseObservation, temperatureC: null })

      expect(wrapper.text()).toContain("—")
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
    it("renders the created date in the description", () => {
      const wrapper = mountComponent()

      // formatDate("2024-03-01T00:00:00Z") → "Mar 1, 2024" (or similar)
      expect(wrapper.text()).toMatch(/Mar.*2024|2024.*Mar/)
    })
  })
})
