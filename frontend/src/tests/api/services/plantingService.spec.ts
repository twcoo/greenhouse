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
import { plantingService } from "@/api/services/plantingService"

const mockPlanting = {
  id: 1,
  crop: 1,
  cropName: "Tomato",
  variety: 1,
  varietyName: "Sun Gold",
  status: "ACTIVE",
  currentLocation: null,
  hasDailyObservation: false,
  createdAt: "2024-01-01T00:00:00Z",
}

const paginatedResponse = {
  data: { data: { results: [mockPlanting], count: 1, next: null, previous: null } },
}

beforeEach(() => {
  vi.clearAllMocks()
})

describe("plantingService", () => {
  describe("getAll", () => {
    it("calls GET /plantings/ with default params", async () => {
      vi.mocked(apiClient.get).mockResolvedValue(paginatedResponse)

      const result = await plantingService.getAll()

      expect(apiClient.get).toHaveBeenCalledWith("/plantings/", {
        params: { page: 1, page_size: 10, search: undefined },
      })
      expect(result).toEqual(paginatedResponse.data.data)
    })

    it("passes custom page, pageSize, and search params", async () => {
      vi.mocked(apiClient.get).mockResolvedValue(paginatedResponse)

      await plantingService.getAll(2, 25, "tomato")

      expect(apiClient.get).toHaveBeenCalledWith("/plantings/", {
        params: { page: 2, page_size: 25, search: "tomato" },
      })
    })

    it("passes search as undefined when empty string", async () => {
      vi.mocked(apiClient.get).mockResolvedValue(paginatedResponse)

      await plantingService.getAll(1, 10, "")

      expect(apiClient.get).toHaveBeenCalledWith("/plantings/", {
        params: { page: 1, page_size: 10, search: undefined },
      })
    })
  })

  describe("create", () => {
    it("calls POST /plantings/ with payload", async () => {
      vi.mocked(apiClient.post).mockResolvedValue({ data: {} })

      const payload = { crop: 1, variety: 1 }

      await plantingService.create(payload)

      expect(apiClient.post).toHaveBeenCalledWith("/plantings/", payload)
    })
  })

  describe("update", () => {
    it("calls PUT /plantings/:id with payload", async () => {
      vi.mocked(apiClient.put).mockResolvedValue({ data: {} })

      const payload = { crop: 1, variety: 2 }

      await plantingService.update(1, payload)

      expect(apiClient.put).toHaveBeenCalledWith("/plantings/1", payload)
    })
  })

  describe("delete", () => {
    it("calls DELETE /plantings/:id", async () => {
      vi.mocked(apiClient.delete).mockResolvedValue({ data: {} })

      await plantingService.delete(1)

      expect(apiClient.delete).toHaveBeenCalledWith("/plantings/1")
    })
  })
})
