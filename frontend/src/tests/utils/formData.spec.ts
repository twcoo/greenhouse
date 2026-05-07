import { describe, it, expect } from "vitest"
import { toFormData } from "@/utils/formData"

describe("toFormData", () => {
  it("appends string values as-is", () => {
    const result = toFormData({ name: "tomato" })

    expect(result.get("name")).toBe("tomato")
  })

  it("decamelizes keys", () => {
    const result = toFormData({ healthStatus: "GOOD", soilMoisturePercent: "55.00" })

    expect(result.get("health_status")).toBe("GOOD")
    expect(result.get("soil_moisture_percent")).toBe("55.00")
  })

  it("appends number values as strings", () => {
    const result = toFormData({ leafCount: 8 })

    expect(result.get("leaf_count")).toBe("8")
  })

  it("appends boolean values as strings", () => {
    const trueResult = toFormData({ diseaseSymptoms: true })
    const falseResult = toFormData({ diseaseSymptoms: false })

    expect(trueResult.get("disease_symptoms")).toBe("true")
    expect(falseResult.get("disease_symptoms")).toBe("false")
  })

  it("skips null values", () => {
    const result = toFormData({ heightCm: null })

    expect(result.get("height_cm")).toBeNull()
  })

  it("skips undefined values", () => {
    const result = toFormData({ notes: undefined })

    expect(result.get("notes")).toBeNull()
  })

  it("appends File instances directly", () => {
    const file = new File(["content"], "photo.jpg", { type: "image/jpeg" })
    const result = toFormData({ image: file })

    expect(result.get("image")).toBe(file)
  })

  it("handles a mixed payload", () => {
    const file = new File(["content"], "photo.jpg", { type: "image/jpeg" })
    const result = toFormData({
      healthStatus: "GOOD",
      leafCount: 5,
      diseaseSymptoms: false,
      heightCm: null,
      notes: undefined,
      image: file,
    })

    expect(result.get("health_status")).toBe("GOOD")
    expect(result.get("leaf_count")).toBe("5")
    expect(result.get("disease_symptoms")).toBe("false")
    expect(result.get("height_cm")).toBeNull()
    expect(result.get("notes")).toBeNull()
    expect(result.get("image")).toBe(file)
  })
})
