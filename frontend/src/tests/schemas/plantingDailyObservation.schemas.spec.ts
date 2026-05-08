import { describe, it, expect } from "vitest"
import { plantingDailyObservationSchema } from "@/schemas/plantingDailyObservation.schemas"

const validBase = {
  healthStatus: "GOOD" as const,
  pestPressure: "NONE" as const,
  diseaseSymptoms: false,
}

describe("plantingDailyObservationSchema", () => {
  describe("valid input", () => {
    it("parses a minimal valid form with defaults only", () => {
      const result = plantingDailyObservationSchema.safeParse(validBase)

      expect(result.success).toBe(true)
    })

    it("parses a fully populated form", () => {
      const result = plantingDailyObservationSchema.safeParse({
        ...validBase,
        heightCm: 15.5,
        leafCount: 3,
        temperatureC: 22.5,
        humidityPercent: 65.0,
        lightHours: 8.0,
        soilMoisturePercent: 40.0,
        soilPh: 6.5,
        ecMsCm: 1.2,
        notes: "Healthy plant",
      })

      expect(result.success).toBe(true)
      if (result.success) {
        expect(result.data.heightCm).toBe(15.5)
        expect(result.data.leafCount).toBe(3)
        expect(result.data.ecMsCm).toBe(1.2)
      }
    })

    it("passes diseaseSymptoms = true through without overriding to false", () => {
      const result = plantingDailyObservationSchema.safeParse({
        ...validBase,
        diseaseSymptoms: true,
      })

      expect(result.success).toBe(true)
      if (result.success) {
        expect(result.data.diseaseSymptoms).toBe(true)
      }
    })

    it("coerces string number to number for decimal fields", () => {
      const result = plantingDailyObservationSchema.safeParse({
        ...validBase,
        heightCm: "12.5",
        temperatureC: "22.0",
      })

      expect(result.success).toBe(true)
      if (result.success) {
        expect(result.data.heightCm).toBe(12.5)
        expect(result.data.temperatureC).toBe(22.0)
      }
    })
  })

  describe("empty string coercion", () => {
    it("coerces empty string to undefined for decimal fields", () => {
      const result = plantingDailyObservationSchema.safeParse({
        ...validBase,
        heightCm: "",
        temperatureC: "",
        humidityPercent: "",
        lightHours: "",
        soilMoisturePercent: "",
        soilPh: "",
        ecMsCm: "",
      })

      expect(result.success).toBe(true)
      if (result.success) {
        expect(result.data.heightCm).toBeUndefined()
        expect(result.data.temperatureC).toBeUndefined()
        expect(result.data.humidityPercent).toBeUndefined()
        expect(result.data.soilPh).toBeUndefined()
      }
    })

    it("coerces empty string to undefined for leafCount", () => {
      const result = plantingDailyObservationSchema.safeParse({
        ...validBase,
        leafCount: "",
      })

      expect(result.success).toBe(true)
      if (result.success) {
        expect(result.data.leafCount).toBeUndefined()
      }
    })
  })

  describe("enum validation", () => {
    it("fails when healthStatus is not a valid enum value", () => {
      const result = plantingDailyObservationSchema.safeParse({
        ...validBase,
        healthStatus: "INVALID",
      })

      expect(result.success).toBe(false)
    })

    it("fails when pestPressure is not a valid enum value", () => {
      const result = plantingDailyObservationSchema.safeParse({
        ...validBase,
        pestPressure: "VERY_HIGH",
      })

      expect(result.success).toBe(false)
    })

    it("accepts all valid healthStatus values", () => {
      for (const status of ["GOOD", "FAIR", "POOR"]) {
        const result = plantingDailyObservationSchema.safeParse({
          ...validBase,
          healthStatus: status,
        })
        expect(result.success).toBe(true)
      }
    })

    it("accepts all valid pestPressure values", () => {
      for (const pressure of ["NONE", "LOW", "MEDIUM", "HIGH"]) {
        const result = plantingDailyObservationSchema.safeParse({
          ...validBase,
          pestPressure: pressure,
        })
        expect(result.success).toBe(true)
      }
    })
  })

  describe("leafCount validation", () => {
    it("fails for a negative leafCount", () => {
      const result = plantingDailyObservationSchema.safeParse({
        ...validBase,
        leafCount: -1,
      })

      expect(result.success).toBe(false)
    })

    it("fails for a non-integer leafCount", () => {
      const result = plantingDailyObservationSchema.safeParse({
        ...validBase,
        leafCount: 2.5,
      })

      expect(result.success).toBe(false)
    })

    it("accepts zero leafCount", () => {
      const result = plantingDailyObservationSchema.safeParse({
        ...validBase,
        leafCount: 0,
      })

      expect(result.success).toBe(true)
      if (result.success) {
        expect(result.data.leafCount).toBe(0)
      }
    })
  })
})
