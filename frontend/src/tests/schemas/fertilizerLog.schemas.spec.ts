import { describe, it, expect } from "vitest"
import { fertilizerLogSchema } from "@/schemas/fertilizerLog.schemas"

describe("fertilizerLogSchema", () => {
  it("accepts a valid log entry", () => {
    const result = fertilizerLogSchema.safeParse({
      logDate: "2024-03-01",
      eventType: "ADDED_INGREDIENT",
      itemAdded: "banana peels",
      quantity: "2 kg",
      notes: "Chopped first.",
    })
    expect(result.success).toBe(true)
  })

  it("applies default event type when omitted", () => {
    const result = fertilizerLogSchema.safeParse({ logDate: "2024-03-01" })
    expect(result.success).toBe(true)
    if (result.success) {
      expect(result.data.eventType).toBe("OTHER")
    }
  })

  it("rejects invalid logDate", () => {
    const result = fertilizerLogSchema.safeParse({ logDate: "not-a-date" })
    expect(result.success).toBe(false)
  })

  it("rejects invalid event type", () => {
    const result = fertilizerLogSchema.safeParse({
      logDate: "2024-03-01",
      eventType: "UNKNOWN",
    })
    expect(result.success).toBe(false)
  })
})
