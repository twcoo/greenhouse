import { describe, it, expect, vi, beforeEach } from "vitest"

vi.mock("@/api/client", () => ({
  apiClient: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  },
}))

import { apiClient } from "@/api/client"
import { plantingDailyObservationService } from "@/api/services/plantingDailyObservationService"

const mockObservation = {
  id: 1,
  stage: null,
  stageName: null,
  healthStatus: "GOOD",
  pestPressure: "NONE",
  diseaseSymptoms: false,
  heightCm: "15.50",
  leafCount: 3,
  temperatureC: null,
  humidityPercent: null,
  lightHours: null,
  soilMoisturePercent: null,
  soilPh: null,
  ecMsCm: null,
  notes: "Looking healthy",
  image: null,
  createdAt: "2024-03-01T00:00:00Z",
  updatedAt: "2024-03-01T00:00:00Z",
}

const paginatedResponse = {
  data: { data: { results: [mockObservation], count: 1, next: null, previous: null } },
}

beforeEach(() => {
  vi.clearAllMocks()
})

describe("plantingDailyObservationService", () => {
  describe("getAll", () => {
    it("calls GET /plantings/:plantingId/observations/ with page_size 100", async () => {
      vi.mocked(apiClient.get).mockResolvedValue(paginatedResponse)

      const result = await plantingDailyObservationService.getAll(5)

      expect(apiClient.get).toHaveBeenCalledWith("/plantings/5/observations/", {
        params: { page_size: 100 },
      })
      expect(result).toEqual(paginatedResponse.data.data)
    })
  })

  describe("create", () => {
    it("calls POST /plantings/:plantingId/observations/ with FormData and multipart header", async () => {
      vi.mocked(apiClient.post).mockResolvedValue({ data: { data: mockObservation } })

      await plantingDailyObservationService.create(5, {
        healthStatus: "GOOD",
        pestPressure: "NONE",
        diseaseSymptoms: false,
      })

      expect(apiClient.post).toHaveBeenCalledWith(
        "/plantings/5/observations/",
        expect.any(FormData),
        { headers: { "Content-Type": "multipart/form-data" } },
      )
    })

    it("appends healthStatus and pestPressure to FormData", async () => {
      vi.mocked(apiClient.post).mockResolvedValue({ data: { data: mockObservation } })

      await plantingDailyObservationService.create(5, {
        healthStatus: "POOR",
        pestPressure: "HIGH",
        diseaseSymptoms: false,
      })

      const formData = vi.mocked(apiClient.post).mock.calls[0][1] as FormData
      expect(formData.get("health_status")).toBe("POOR")
      expect(formData.get("pest_pressure")).toBe("HIGH")
    })

    it("appends diseaseSymptoms to FormData", async () => {
      vi.mocked(apiClient.post).mockResolvedValue({ data: { data: mockObservation } })

      await plantingDailyObservationService.create(5, {
        healthStatus: "GOOD",
        pestPressure: "NONE",
        diseaseSymptoms: true,
      })

      const formData = vi.mocked(apiClient.post).mock.calls[0][1] as FormData
      expect(formData.get("disease_symptoms")).toBe("true")
    })

    it("appends optional numeric fields when provided", async () => {
      vi.mocked(apiClient.post).mockResolvedValue({ data: { data: mockObservation } })

      await plantingDailyObservationService.create(5, {
        healthStatus: "GOOD",
        pestPressure: "NONE",
        diseaseSymptoms: false,
        heightCm: 15.5,
        leafCount: 3,
        temperatureC: 22.0,
      })

      const formData = vi.mocked(apiClient.post).mock.calls[0][1] as FormData
      expect(formData.get("height_cm")).toBe("15.5")
      expect(formData.get("leaf_count")).toBe("3")
      expect(formData.get("temperature_c")).toBe("22")
    })

    it("does not append optional fields when absent", async () => {
      vi.mocked(apiClient.post).mockResolvedValue({ data: { data: mockObservation } })

      await plantingDailyObservationService.create(5, {
        healthStatus: "GOOD",
        pestPressure: "NONE",
        diseaseSymptoms: false,
      })

      const formData = vi.mocked(apiClient.post).mock.calls[0][1] as FormData
      expect(formData.get("height_cm")).toBeNull()
      expect(formData.get("leaf_count")).toBeNull()
    })

    it("appends image when provided", async () => {
      vi.mocked(apiClient.post).mockResolvedValue({ data: { data: mockObservation } })

      const file = new File(["content"], "photo.jpg", { type: "image/jpeg" })
      await plantingDailyObservationService.create(5, {
        healthStatus: "GOOD",
        pestPressure: "NONE",
        diseaseSymptoms: false,
        image: file,
      })

      const formData = vi.mocked(apiClient.post).mock.calls[0][1] as FormData
      expect(formData.get("image")).toBe(file)
    })

    it("does not append image when absent", async () => {
      vi.mocked(apiClient.post).mockResolvedValue({ data: { data: mockObservation } })

      await plantingDailyObservationService.create(5, {
        healthStatus: "GOOD",
        pestPressure: "NONE",
        diseaseSymptoms: false,
      })

      const formData = vi.mocked(apiClient.post).mock.calls[0][1] as FormData
      expect(formData.get("image")).toBeNull()
    })

    it("returns the observation from the response", async () => {
      vi.mocked(apiClient.post).mockResolvedValue({ data: { data: mockObservation } })

      const result = await plantingDailyObservationService.create(5, {
        healthStatus: "GOOD",
        pestPressure: "NONE",
        diseaseSymptoms: false,
      })

      expect(result).toEqual(mockObservation)
    })
  })

  describe("update", () => {
    it("calls PUT /plantings/:plantingId/observations/:id with FormData and multipart header", async () => {
      vi.mocked(apiClient.put).mockResolvedValue({ data: { data: mockObservation } })

      await plantingDailyObservationService.update(5, 1, {
        healthStatus: "FAIR",
        pestPressure: "LOW",
        diseaseSymptoms: true,
      })

      expect(apiClient.put).toHaveBeenCalledWith(
        "/plantings/5/observations/1",
        expect.any(FormData),
        { headers: { "Content-Type": "multipart/form-data" } },
      )
    })

    it("appends updated fields to FormData", async () => {
      vi.mocked(apiClient.put).mockResolvedValue({ data: { data: mockObservation } })

      await plantingDailyObservationService.update(5, 1, {
        healthStatus: "FAIR",
        pestPressure: "LOW",
        diseaseSymptoms: true,
        notes: "Yellowing on lower leaves",
      })

      const formData = vi.mocked(apiClient.put).mock.calls[0][1] as FormData
      expect(formData.get("health_status")).toBe("FAIR")
      expect(formData.get("disease_symptoms")).toBe("true")
      expect(formData.get("notes")).toBe("Yellowing on lower leaves")
    })

    it("returns the updated observation from the response", async () => {
      vi.mocked(apiClient.put).mockResolvedValue({ data: { data: mockObservation } })

      const result = await plantingDailyObservationService.update(5, 1, {
        healthStatus: "GOOD",
        pestPressure: "NONE",
        diseaseSymptoms: false,
      })

      expect(result).toEqual(mockObservation)
    })
  })

  describe("delete", () => {
    it("calls DELETE /plantings/:plantingId/observations/:id", async () => {
      vi.mocked(apiClient.delete).mockResolvedValue({ data: {} })

      await plantingDailyObservationService.delete(5, 1)

      expect(apiClient.delete).toHaveBeenCalledWith("/plantings/5/observations/1")
    })
  })
})
