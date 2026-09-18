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
import { fertilizerLogService } from "@/api/services/fertilizerLogService"

const mockLog = {
  id: 1,
  eventType: "ADDED_INGREDIENT",
  itemAdded: "banana peels",
  quantity: "2 kg",
  notes: "Chopped first.",
  logDate: "2024-03-01",
  createdAt: "2024-03-01T00:00:00Z",
  updatedAt: "2024-03-01T00:00:00Z",
}

const paginatedResponse = {
  data: { data: { results: [mockLog], count: 1, next: null, previous: null } },
}

beforeEach(() => {
  vi.clearAllMocks()
})

describe("fertilizerLogService", () => {
  describe("getAll", () => {
    it("calls GET /fertilizers/:id/logs/ with default params", async () => {
      vi.mocked(apiClient.get).mockResolvedValue(paginatedResponse)

      const result = await fertilizerLogService.getAll(5)

      expect(apiClient.get).toHaveBeenCalledWith("/fertilizers/5/logs/", {
        params: { page: 1, page_size: 10 },
      })
      expect(result).toEqual(paginatedResponse.data.data)
    })
  })

  describe("create", () => {
    it("calls POST /fertilizers/:id/logs/ with payload and returns log", async () => {
      vi.mocked(apiClient.post).mockResolvedValue({ data: { data: mockLog } })

      const payload = { eventType: "ADDED_WATER", quantity: "5 liters" }

      const result = await fertilizerLogService.create(5, payload)

      expect(apiClient.post).toHaveBeenCalledWith("/fertilizers/5/logs/", payload)
      expect(result).toEqual(mockLog)
    })
  })

  describe("update", () => {
    it("calls PUT /fertilizers/:id/logs/:logId with payload", async () => {
      vi.mocked(apiClient.put).mockResolvedValue({ data: { data: mockLog } })

      const payload = { notes: "Updated." }

      const result = await fertilizerLogService.update(5, 1, payload)

      expect(apiClient.put).toHaveBeenCalledWith("/fertilizers/5/logs/1", payload)
      expect(result).toEqual(mockLog)
    })
  })

  describe("delete", () => {
    it("calls DELETE /fertilizers/:id/logs/:logId", async () => {
      vi.mocked(apiClient.delete).mockResolvedValue({ data: {} })

      await fertilizerLogService.delete(5, 1)

      expect(apiClient.delete).toHaveBeenCalledWith("/fertilizers/5/logs/1")
    })
  })
})
