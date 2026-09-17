import { describe, it, expect } from "vitest"
import { fertilizerSchema } from "@/schemas/fertilizer.schemas"

const validBase = {
  name: "Swamp Fertilizer #1",
  type: "SWAMP",
  status: "BREWING",
  startDate: "2024-01-01",
  ingredients: ["banana peels"],
}

describe("fertilizerSchema", () => {
  it("accepts a valid fertilizer", () => {
    const result = fertilizerSchema.safeParse(validBase)
    expect(result.success).toBe(true)
  })

  it("applies default type, status, and ingredients when omitted", () => {
    const result = fertilizerSchema.safeParse({
      name: "Swamp Fertilizer #1",
      startDate: "2024-01-01",
    })
    expect(result.success).toBe(true)
    if (result.success) {
      expect(result.data.type).toBe("SWAMP")
      expect(result.data.status).toBe("BREWING")
      expect(result.data.ingredients).toEqual([])
    }
  })

  it("rejects empty name", () => {
    const result = fertilizerSchema.safeParse({ ...validBase, name: "" })
    expect(result.success).toBe(false)
    if (!result.success) {
      expect(result.error.issues.map((i) => i.path[0])).toContain("name")
    }
  })

  it("rejects invalid type", () => {
    const result = fertilizerSchema.safeParse({ ...validBase, type: "UNKNOWN" })
    expect(result.success).toBe(false)
  })

  it("rejects invalid status", () => {
    const result = fertilizerSchema.safeParse({ ...validBase, status: "UNKNOWN" })
    expect(result.success).toBe(false)
  })

  it("rejects invalid startDate", () => {
    const result = fertilizerSchema.safeParse({ ...validBase, startDate: "not-a-date" })
    expect(result.success).toBe(false)
  })
})
