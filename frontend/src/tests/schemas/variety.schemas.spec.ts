import { describe, it, expect } from "vitest"
import { varietySchema } from "@/schemas/variety.schemas"

describe("varietySchema", () => {
  describe("valid data", () => {
    it("accepts a valid variety", () => {
      const result = varietySchema.safeParse({
        name: "Sun Gold",
        crop: 1,
        growthHabit: ["INDETERMINATE"],
      })
      expect(result.success).toBe(true)
    })

    it("accepts multiple growth habits", () => {
      const result = varietySchema.safeParse({
        name: "Cherokee Purple",
        crop: 2,
        growthHabit: ["DETERMINATE", "INDETERMINATE"],
      })
      expect(result.success).toBe(true)
    })
  })

  describe("name validation", () => {
    it("rejects empty name", () => {
      const result = varietySchema.safeParse({
        name: "",
        crop: 1,
        growthHabit: ["DETERMINATE"],
      })
      expect(result.success).toBe(false)
      if (!result.success) {
        const fields = result.error.issues.map((i) => i.path[0])
        expect(fields).toContain("name")
      }
    })
  })

  describe("crop validation", () => {
    it("rejects crop = 0", () => {
      const result = varietySchema.safeParse({
        name: "Sun Gold",
        crop: 0,
        growthHabit: ["DETERMINATE"],
      })
      expect(result.success).toBe(false)
      if (!result.success) {
        const fields = result.error.issues.map((i) => i.path[0])
        expect(fields).toContain("crop")
      }
    })
  })

  describe("growthHabit validation", () => {
    it("rejects empty growthHabit array", () => {
      const result = varietySchema.safeParse({
        name: "Sun Gold",
        crop: 1,
        growthHabit: [],
      })
      expect(result.success).toBe(false)
      if (!result.success) {
        const fields = result.error.issues.map((i) => i.path[0])
        expect(fields).toContain("growthHabit")
      }
    })

    it("rejects invalid growthHabit enum value", () => {
      const result = varietySchema.safeParse({
        name: "Sun Gold",
        crop: 1,
        growthHabit: ["INVALID_VALUE"],
      })
      expect(result.success).toBe(false)
    })
  })
})
