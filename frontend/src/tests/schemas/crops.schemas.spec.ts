import { describe, it, expect } from "vitest"
import { cropsSchema } from "@/schemas/crops.schemas"

describe("cropsSchema", () => {
  describe("valid data", () => {
    it("accepts a valid crop", () => {
      const result = cropsSchema.safeParse({
        name: "Tomato",
        scientificName: "Solanum lycopersicum",
        category: "VEGETABLE",
        sunlightRequirement: "FULL SUN",
        minDaysToHarvest: 60,
        maxDaysToHarvest: 90,
      })
      expect(result.success).toBe(true)
    })

    it("accepts all valid category values", () => {
      for (const category of ["VEGETABLE", "FRUIT"]) {
        const result = cropsSchema.safeParse({
          name: "Tomato",
          scientificName: "Solanum lycopersicum",
          category,
          sunlightRequirement: "FULL SUN",
          minDaysToHarvest: 60,
          maxDaysToHarvest: 90,
        })
        expect(result.success).toBe(true)
      }
    })

    it("accepts all valid sunlight requirement values", () => {
      for (const sunlightRequirement of ["FULL SUN", "PART SUN", "FULL SHADE"]) {
        const result = cropsSchema.safeParse({
          name: "Tomato",
          scientificName: "Solanum lycopersicum",
          category: "VEGETABLE",
          sunlightRequirement,
          minDaysToHarvest: 60,
          maxDaysToHarvest: 90,
        })
        expect(result.success).toBe(true)
      }
    })
  })

  describe("name validation", () => {
    it("rejects empty name", () => {
      const result = cropsSchema.safeParse({
        name: "",
        scientificName: "Solanum lycopersicum",
        category: "VEGETABLE",
        sunlightRequirement: "FULL SUN",
        minDaysToHarvest: 60,
        maxDaysToHarvest: 90,
      })
      expect(result.success).toBe(false)
      if (!result.success) {
        const fields = result.error.issues.map((i) => i.path[0])
        expect(fields).toContain("name")
      }
    })
  })

  describe("scientificName validation", () => {
    it("rejects empty scientific name", () => {
      const result = cropsSchema.safeParse({
        name: "Tomato",
        scientificName: "",
        category: "VEGETABLE",
        sunlightRequirement: "FULL SUN",
        minDaysToHarvest: 60,
        maxDaysToHarvest: 90,
      })
      expect(result.success).toBe(false)
      if (!result.success) {
        const fields = result.error.issues.map((i) => i.path[0])
        expect(fields).toContain("scientificName")
      }
    })
  })

  describe("category validation", () => {
    it("rejects an invalid category", () => {
      const result = cropsSchema.safeParse({
        name: "Tomato",
        scientificName: "Solanum lycopersicum",
        category: "HERB",
        sunlightRequirement: "FULL SUN",
        minDaysToHarvest: 60,
        maxDaysToHarvest: 90,
      })
      expect(result.success).toBe(false)
      if (!result.success) {
        const fields = result.error.issues.map((i) => i.path[0])
        expect(fields).toContain("category")
      }
    })
  })

  describe("sunlightRequirement validation", () => {
    it("rejects an invalid sunlight requirement", () => {
      const result = cropsSchema.safeParse({
        name: "Tomato",
        scientificName: "Solanum lycopersicum",
        category: "VEGETABLE",
        sunlightRequirement: "DEEP SHADE",
        minDaysToHarvest: 60,
        maxDaysToHarvest: 90,
      })
      expect(result.success).toBe(false)
      if (!result.success) {
        const fields = result.error.issues.map((i) => i.path[0])
        expect(fields).toContain("sunlightRequirement")
      }
    })
  })

  describe("days to harvest validation", () => {
    it("rejects minDaysToHarvest less than 1", () => {
      const result = cropsSchema.safeParse({
        name: "Tomato",
        scientificName: "Solanum lycopersicum",
        category: "VEGETABLE",
        sunlightRequirement: "FULL SUN",
        minDaysToHarvest: 0,
        maxDaysToHarvest: 90,
      })
      expect(result.success).toBe(false)
      if (!result.success) {
        const fields = result.error.issues.map((i) => i.path[0])
        expect(fields).toContain("minDaysToHarvest")
      }
    })

    it("rejects maxDaysToHarvest less than 1", () => {
      const result = cropsSchema.safeParse({
        name: "Tomato",
        scientificName: "Solanum lycopersicum",
        category: "VEGETABLE",
        sunlightRequirement: "FULL SUN",
        minDaysToHarvest: 60,
        maxDaysToHarvest: 0,
      })
      expect(result.success).toBe(false)
      if (!result.success) {
        const fields = result.error.issues.map((i) => i.path[0])
        expect(fields).toContain("maxDaysToHarvest")
      }
    })

    it("rejects maxDaysToHarvest less than minDaysToHarvest", () => {
      const result = cropsSchema.safeParse({
        name: "Tomato",
        scientificName: "Solanum lycopersicum",
        category: "VEGETABLE",
        sunlightRequirement: "FULL SUN",
        minDaysToHarvest: 90,
        maxDaysToHarvest: 60,
      })
      expect(result.success).toBe(false)
      if (!result.success) {
        const fields = result.error.issues.map((i) => i.path[0])
        expect(fields).toContain("maxDaysToHarvest")
      }
    })

    it("accepts equal min and max days to harvest", () => {
      const result = cropsSchema.safeParse({
        name: "Tomato",
        scientificName: "Solanum lycopersicum",
        category: "VEGETABLE",
        sunlightRequirement: "FULL SUN",
        minDaysToHarvest: 75,
        maxDaysToHarvest: 75,
      })
      expect(result.success).toBe(true)
    })
  })
})
