import { describe, it, expect } from "vitest"
import { plantingLocationSchema } from "@/schemas/plantingLocation.schemas"

describe("plantingLocationSchema", () => {
  describe("valid data", () => {
    it("accepts a valid POT location", () => {
      const result = plantingLocationSchema.safeParse({
        name: "My Pot",
        locationType: "POT",
        width: 20,
        height: 30,
      })
      expect(result.success).toBe(true)
    })

    it("accepts a valid NURSERYPOT location", () => {
      const result = plantingLocationSchema.safeParse({
        name: "Seedling Tray",
        locationType: "NURSERYPOT",
        width: 10,
        height: 15,
      })
      expect(result.success).toBe(true)
    })

    it("accepts a valid GROUND location", () => {
      const result = plantingLocationSchema.safeParse({
        name: "Garden Bed",
        locationType: "GROUND",
        width: 100,
        length: 200,
      })
      expect(result.success).toBe(true)
    })
  })

  describe("name validation", () => {
    it("rejects empty name", () => {
      const result = plantingLocationSchema.safeParse({
        name: "",
        locationType: "POT",
        width: 20,
        height: 10,
      })
      expect(result.success).toBe(false)
      if (!result.success) {
        const fields = result.error.issues.map((i) => i.path[0])
        expect(fields).toContain("name")
      }
    })
  })

  describe("width validation", () => {
    it("rejects width of 0", () => {
      const result = plantingLocationSchema.safeParse({
        name: "Test",
        locationType: "POT",
        width: 0,
        height: 10,
      })
      expect(result.success).toBe(false)
      if (!result.success) {
        const fields = result.error.issues.map((i) => i.path[0])
        expect(fields).toContain("width")
      }
    })
  })

  describe("type-specific field requirements", () => {
    it("rejects GROUND without length", () => {
      const result = plantingLocationSchema.safeParse({
        name: "Garden Bed",
        locationType: "GROUND",
        width: 100,
      })
      expect(result.success).toBe(false)
      if (!result.success) {
        const fields = result.error.issues.map((i) => i.path[0])
        expect(fields).toContain("length")
      }
    })

    it("rejects POT without height", () => {
      const result = plantingLocationSchema.safeParse({
        name: "My Pot",
        locationType: "POT",
        width: 20,
      })
      expect(result.success).toBe(false)
      if (!result.success) {
        const fields = result.error.issues.map((i) => i.path[0])
        expect(fields).toContain("height")
      }
    })

    it("rejects NURSERYPOT without height", () => {
      const result = plantingLocationSchema.safeParse({
        name: "Seedling Tray",
        locationType: "NURSERYPOT",
        width: 10,
      })
      expect(result.success).toBe(false)
      if (!result.success) {
        const fields = result.error.issues.map((i) => i.path[0])
        expect(fields).toContain("height")
      }
    })
  })
})
