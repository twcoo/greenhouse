import { describe, it, expect } from "vitest"
import { plantingDailyObservationSchema } from "@/schemas/plantingDailyObservation.schemas"

const validBase = {
  observationDate: "2024-03-15",
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
        rained: true,
        notes: "Healthy plant",
      })

      expect(result.success).toBe(true)
      if (result.success) {
        expect(result.data.rained).toBe(true)
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
  })

  describe("pruned field", () => {
    it("defaults pruned to false when omitted", () => {
      const result = plantingDailyObservationSchema.safeParse(validBase)

      expect(result.success).toBe(true)
      if (result.success) {
        expect(result.data.pruned).toBe(false)
      }
    })

    it("defaults pruned to false when null", () => {
      const result = plantingDailyObservationSchema.safeParse({
        ...validBase,
        pruned: null,
      })

      expect(result.success).toBe(true)
      if (result.success) {
        expect(result.data.pruned).toBe(false)
      }
    })

    it("passes pruned = true correctly", () => {
      const result = plantingDailyObservationSchema.safeParse({
        ...validBase,
        pruned: true,
      })

      expect(result.success).toBe(true)
      if (result.success) {
        expect(result.data.pruned).toBe(true)
      }
    })

    it("pruningDetail is optional", () => {
      const result = plantingDailyObservationSchema.safeParse({
        ...validBase,
        pruned: true,
      })

      expect(result.success).toBe(true)
      if (result.success) {
        expect(result.data.pruningDetail).toBeUndefined()
      }
    })

    it("passes pruningDetail when provided", () => {
      const result = plantingDailyObservationSchema.safeParse({
        ...validBase,
        pruned: true,
        pruningDetail: "removed lower leaves",
      })

      expect(result.success).toBe(true)
      if (result.success) {
        expect(result.data.pruningDetail).toBe("removed lower leaves")
      }
    })
  })

  describe("rained field", () => {
    it("defaults rained to false when omitted", () => {
      const result = plantingDailyObservationSchema.safeParse(validBase)

      expect(result.success).toBe(true)
      if (result.success) {
        expect(result.data.rained).toBe(false)
      }
    })

    it("defaults rained to false when null", () => {
      const result = plantingDailyObservationSchema.safeParse({
        ...validBase,
        rained: null,
      })

      expect(result.success).toBe(true)
      if (result.success) {
        expect(result.data.rained).toBe(false)
      }
    })

    it("passes rained = true correctly", () => {
      const result = plantingDailyObservationSchema.safeParse({
        ...validBase,
        rained: true,
      })

      expect(result.success).toBe(true)
      if (result.success) {
        expect(result.data.rained).toBe(true)
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

  describe("observationDate validation", () => {
    it("fails when observationDate is missing", () => {
      const { observationDate: _, ...withoutDate } = validBase
      const result = plantingDailyObservationSchema.safeParse(withoutDate)

      expect(result.success).toBe(false)
    })

    it("fails when observationDate has wrong format", () => {
      const result = plantingDailyObservationSchema.safeParse({
        ...validBase,
        observationDate: "not-a-date",
      })

      expect(result.success).toBe(false)
    })

    it("fails when observationDate uses slashes instead of dashes", () => {
      const result = plantingDailyObservationSchema.safeParse({
        ...validBase,
        observationDate: "2024/03/15",
      })

      expect(result.success).toBe(false)
    })

    it("passes with a valid ISO date string", () => {
      const result = plantingDailyObservationSchema.safeParse({
        ...validBase,
        observationDate: "2024-01-01",
      })

      expect(result.success).toBe(true)
      if (result.success) {
        expect(result.data.observationDate).toBe("2024-01-01")
      }
    })
  })
})
