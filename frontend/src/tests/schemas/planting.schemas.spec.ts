import { describe, it, expect } from "vitest"
import { plantingSchema } from "@/schemas/planting.schemas"

describe("plantingSchema", () => {
  describe("valid data", () => {
    it("accepts valid crop and variety ids", () => {
      const result = plantingSchema.safeParse({ crop: 1, variety: 1 })
      expect(result.success).toBe(true)
    })

    it("coerces string ids to numbers", () => {
      const result = plantingSchema.safeParse({ crop: "1", variety: "2" })
      expect(result.success).toBe(true)
      if (result.success) {
        expect(result.data.crop).toBe(1)
        expect(result.data.variety).toBe(2)
      }
    })
  })

  describe("crop validation", () => {
    it("rejects crop = 0", () => {
      const result = plantingSchema.safeParse({ crop: 0, variety: 1 })
      expect(result.success).toBe(false)
      if (!result.success) {
        expect(result.error.issues.map((i) => i.path[0])).toContain("crop")
      }
    })

    it("rejects missing crop", () => {
      const result = plantingSchema.safeParse({ variety: 1 })
      expect(result.success).toBe(false)
    })
  })

  describe("variety validation", () => {
    it("rejects variety = 0", () => {
      const result = plantingSchema.safeParse({ crop: 1, variety: 0 })
      expect(result.success).toBe(false)
      if (!result.success) {
        expect(result.error.issues.map((i) => i.path[0])).toContain("variety")
      }
    })

    it("rejects missing variety", () => {
      const result = plantingSchema.safeParse({ crop: 1 })
      expect(result.success).toBe(false)
    })
  })

  describe("status validation", () => {
    it.each(["ACTIVE", "HARVESTED", "DEAD", "REMOVED"])("accepts status '%s'", (status) => {
      const result = plantingSchema.safeParse({ crop: 1, variety: 1, status })
      expect(result.success).toBe(true)
    })

    it("allows missing status (optional)", () => {
      const result = plantingSchema.safeParse({ crop: 1, variety: 1 })
      expect(result.success).toBe(true)
    })

    it("rejects invalid status", () => {
      const result = plantingSchema.safeParse({ crop: 1, variety: 1, status: "INVALID" })
      expect(result.success).toBe(false)
      if (!result.success) {
        expect(result.error.issues.map((i) => i.path[0])).toContain("status")
      }
    })
  })
})
