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
import { fertilizerService } from "@/api/services/fertilizerService"

const mockFertilizer = {
  id: 1,
  name: "Swamp Fertilizer #1",
  type: "SWAMP",
  status: "BREWING",
  startDate: "2024-01-01",
  ingredients: ["banana peels", "molasses"],
  notes: "",
  createdAt: "2024-01-01T00:00:00Z",
  updatedAt: "2024-01-01T00:00:00Z",
}

const paginatedResponse = {
  data: { data: { results: [mockFertilizer], count: 1, next: null, previous: null } },
}

beforeEach(() => {
  vi.clearAllMocks()
})

describe("fertilizerService", () => {
  describe("getAll", () => {
    it("calls GET /fertilizers/ with default params", async () => {
      vi.mocked(apiClient.get).mockResolvedValue(paginatedResponse)

      const result = await fertilizerService.getAll()

      expect(apiClient.get).toHaveBeenCalledWith("/fertilizers/", {
        params: { page: 1, page_size: 10, search: undefined },
      })
      expect(result).toEqual(paginatedResponse.data.data)
    })

    it("passes custom page, pageSize, and search params", async () => {
      vi.mocked(apiClient.get).mockResolvedValue(paginatedResponse)

      await fertilizerService.getAll(2, 25, "swamp")

      expect(apiClient.get).toHaveBeenCalledWith("/fertilizers/", {
        params: { page: 2, page_size: 25, search: "swamp" },
      })
    })
  })

  describe("create", () => {
    it("calls POST /fertilizers/ with payload", async () => {
      vi.mocked(apiClient.post).mockResolvedValue({ data: {} })

      const payload = { name: "Swamp Fertilizer #1" }

      await fertilizerService.create(payload)

      expect(apiClient.post).toHaveBeenCalledWith("/fertilizers/", payload)
    })
  })

  describe("update", () => {
    it("calls PUT /fertilizers/:id with payload", async () => {
      vi.mocked(apiClient.put).mockResolvedValue({ data: {} })

      const payload = { name: "Updated", status: "READY" }

      await fertilizerService.update(1, payload)

      expect(apiClient.put).toHaveBeenCalledWith("/fertilizers/1", payload)
    })
  })

  describe("delete", () => {
    it("calls DELETE /fertilizers/:id", async () => {
      vi.mocked(apiClient.delete).mockResolvedValue({ data: {} })

      await fertilizerService.delete(1)

      expect(apiClient.delete).toHaveBeenCalledWith("/fertilizers/1")
    })
  })
})
