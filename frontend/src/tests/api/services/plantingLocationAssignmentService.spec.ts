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
import { plantingLocationAssignmentService } from "@/api/services/plantingLocationAssignmentService"

const mockAssignment = {
  id: 1,
  plantingLocation: 2,
  plantingLocationName: "Balcony Pot",
  startDate: "2024-01-01",
  endDate: null,
  createdAt: "2024-01-01T00:00:00Z",
  updatedAt: "2024-01-01T00:00:00Z",
}

const paginatedResponse = {
  data: { data: { results: [mockAssignment], count: 1, next: null, previous: null } },
}

beforeEach(() => {
  vi.clearAllMocks()
})

describe("plantingLocationAssignmentService", () => {
  describe("getAll", () => {
    it("calls GET /plantings/:plantingId/locations/ with default page and page_size", async () => {
      vi.mocked(apiClient.get).mockResolvedValue(paginatedResponse)

      const result = await plantingLocationAssignmentService.getAll(5)

      expect(apiClient.get).toHaveBeenCalledWith("/plantings/5/locations/", {
        params: { page: 1, page_size: 10 },
      })
      expect(result).toEqual(paginatedResponse.data.data)
    })

    it("calls GET with explicit page and page_size when provided", async () => {
      vi.mocked(apiClient.get).mockResolvedValue(paginatedResponse)

      await plantingLocationAssignmentService.getAll(5, 3, 20)

      expect(apiClient.get).toHaveBeenCalledWith("/plantings/5/locations/", {
        params: { page: 3, page_size: 20 },
      })
    })

    it("returns the paginated data from the response", async () => {
      vi.mocked(apiClient.get).mockResolvedValue(paginatedResponse)

      const result = await plantingLocationAssignmentService.getAll(1)

      expect(result.results).toHaveLength(1)
      expect(result.results[0]).toEqual(mockAssignment)
      expect(result.count).toBe(1)
    })
  })

  describe("create", () => {
    it("calls POST /plantings/:plantingId/locations/ with payload", async () => {
      vi.mocked(apiClient.post).mockResolvedValue({ data: {} })

      const payload = { plantingLocation: 2, startDate: "2024-01-01" }

      await plantingLocationAssignmentService.create(5, payload)

      expect(apiClient.post).toHaveBeenCalledWith("/plantings/5/locations/", payload)
    })

    it("calls POST with endDate in payload when provided", async () => {
      vi.mocked(apiClient.post).mockResolvedValue({ data: {} })

      const payload = { plantingLocation: 2, startDate: "2024-01-01", endDate: "2024-06-01" }

      await plantingLocationAssignmentService.create(5, payload)

      expect(apiClient.post).toHaveBeenCalledWith("/plantings/5/locations/", payload)
    })
  })

  describe("update", () => {
    it("calls PUT /plantings/:plantingId/locations/:id with payload", async () => {
      vi.mocked(apiClient.put).mockResolvedValue({ data: {} })

      const payload = { plantingLocation: 2, startDate: "2024-01-01", endDate: "2024-09-01" }

      await plantingLocationAssignmentService.update(5, 1, payload)

      expect(apiClient.put).toHaveBeenCalledWith("/plantings/5/locations/1", payload)
    })
  })

  describe("delete", () => {
    it("calls DELETE /plantings/:plantingId/locations/:id", async () => {
      vi.mocked(apiClient.delete).mockResolvedValue({ data: {} })

      await plantingLocationAssignmentService.delete(5, 1)

      expect(apiClient.delete).toHaveBeenCalledWith("/plantings/5/locations/1")
    })
  })
})
