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
import { cropService } from "@/api/services/cropsService"

const mockCrop = {
  id: 1,
  name: "Tomato",
  scientificName: "Solanum lycopersicum",
  category: "VEGETABLE",
  sunlightRequirement: "FULL_SUN",
  minDaysToHarvest: 60,
  maxDaysToHarvest: 80,
}

const paginatedResponse = {
  data: { data: { results: [mockCrop], count: 1, next: null, previous: null } },
}

beforeEach(() => {
  vi.clearAllMocks()
})

describe("cropService", () => {
  describe("getAll", () => {
    it("calls GET /crops/ with default params", async () => {
      vi.mocked(apiClient.get).mockResolvedValue(paginatedResponse)

      const result = await cropService.getAll()

      expect(apiClient.get).toHaveBeenCalledWith("/crops/", {
        params: { page: 1, page_size: 10, search: undefined },
      })
      expect(result).toEqual(paginatedResponse.data.data)
    })

    it("passes custom page, pageSize, and search params", async () => {
      vi.mocked(apiClient.get).mockResolvedValue(paginatedResponse)

      await cropService.getAll(2, 25, "tomato")

      expect(apiClient.get).toHaveBeenCalledWith("/crops/", {
        params: { page: 2, page_size: 25, search: "tomato" },
      })
    })

    it("passes search as undefined when empty string", async () => {
      vi.mocked(apiClient.get).mockResolvedValue(paginatedResponse)

      await cropService.getAll(1, 10, "")

      expect(apiClient.get).toHaveBeenCalledWith("/crops/", {
        params: { page: 1, page_size: 10, search: undefined },
      })
    })
  })

  describe("create", () => {
    it("calls POST /crops/ with payload", async () => {
      vi.mocked(apiClient.post).mockResolvedValue({ data: {} })

      const payload = {
        name: "Tomato",
        scientificName: "Solanum lycopersicum",
        category: "VEGETABLE",
        sunlightRequirement: "FULL_SUN",
        minDaysToHarvest: 60,
        maxDaysToHarvest: 80,
      }

      await cropService.create(payload)

      expect(apiClient.post).toHaveBeenCalledWith("/crops/", payload)
    })
  })

  describe("update", () => {
    it("calls PUT /crops/:id with payload", async () => {
      vi.mocked(apiClient.put).mockResolvedValue({ data: {} })

      const payload = {
        name: "Tomato Updated",
        scientificName: "Solanum lycopersicum",
        category: "VEGETABLE",
        sunlightRequirement: "FULL_SUN",
        minDaysToHarvest: 65,
        maxDaysToHarvest: 85,
      }

      await cropService.update(1, payload)

      expect(apiClient.put).toHaveBeenCalledWith("/crops/1", payload)
    })
  })

  describe("delete", () => {
    it("calls DELETE /crops/:id", async () => {
      vi.mocked(apiClient.delete).mockResolvedValue({ data: {} })

      await cropService.delete(1)

      expect(apiClient.delete).toHaveBeenCalledWith("/crops/1")
    })
  })
})
