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
import { plantingLocationService } from "@/api/services/plantingLocationService"

const mockLocation = {
  id: 1,
  name: "Garden Pot",
  locationType: "POT",
  width: 30,
  height: 40,
}

const paginatedResponse = {
  data: { data: { results: [mockLocation], count: 1, next: null, previous: null } },
}

beforeEach(() => {
  vi.clearAllMocks()
})

describe("plantingLocationService", () => {
  describe("getAll", () => {
    it("calls GET /planting-locations/ with default params", async () => {
      vi.mocked(apiClient.get).mockResolvedValue(paginatedResponse)

      const result = await plantingLocationService.getAll()

      expect(apiClient.get).toHaveBeenCalledWith("/planting-locations/", {
        params: { page: 1, page_size: 10, search: undefined },
      })
      expect(result).toEqual(paginatedResponse.data.data)
    })

    it("passes custom page, pageSize, and search params", async () => {
      vi.mocked(apiClient.get).mockResolvedValue(paginatedResponse)

      await plantingLocationService.getAll(3, 20, "garden")

      expect(apiClient.get).toHaveBeenCalledWith("/planting-locations/", {
        params: { page: 3, page_size: 20, search: "garden" },
      })
    })

    it("passes search as undefined when empty string", async () => {
      vi.mocked(apiClient.get).mockResolvedValue(paginatedResponse)

      await plantingLocationService.getAll(1, 10, "")

      expect(apiClient.get).toHaveBeenCalledWith("/planting-locations/", {
        params: { page: 1, page_size: 10, search: undefined },
      })
    })
  })

  describe("create", () => {
    it("calls POST /planting-locations/ with payload", async () => {
      vi.mocked(apiClient.post).mockResolvedValue({ data: {} })

      const payload = { name: "Garden Pot", locationType: "POT", width: 30, height: 40 }

      await plantingLocationService.create(payload)

      expect(apiClient.post).toHaveBeenCalledWith("/planting-locations/", payload)
    })
  })

  describe("update", () => {
    it("calls PUT /planting-locations/:id with payload", async () => {
      vi.mocked(apiClient.put).mockResolvedValue({ data: {} })

      const payload = { name: "Garden Pot Updated", locationType: "POT", width: 35, height: 45 }

      await plantingLocationService.update(1, payload)

      expect(apiClient.put).toHaveBeenCalledWith("/planting-locations/1", payload)
    })
  })

  describe("delete", () => {
    it("calls DELETE /planting-locations/:id", async () => {
      vi.mocked(apiClient.delete).mockResolvedValue({ data: {} })

      await plantingLocationService.delete(1)

      expect(apiClient.delete).toHaveBeenCalledWith("/planting-locations/1")
    })
  })
})
