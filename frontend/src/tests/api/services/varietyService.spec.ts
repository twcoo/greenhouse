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
import { varietyService } from "@/api/services/varietyService"

const mockVariety = {
  id: 1,
  name: "Sun Gold",
  crop: 1,
  growthHabit: ["INDETERMINATE"],
}

const paginatedResponse = {
  data: { data: { results: [mockVariety], count: 1, next: null, previous: null } },
}

beforeEach(() => {
  vi.clearAllMocks()
})

describe("varietyService", () => {
  describe("getAll", () => {
    it("calls GET /varieties/ with default params", async () => {
      vi.mocked(apiClient.get).mockResolvedValue(paginatedResponse)

      const result = await varietyService.getAll()

      expect(apiClient.get).toHaveBeenCalledWith("/varieties/", {
        params: { page: 1, page_size: 10, search: undefined },
      })
      expect(result).toEqual(paginatedResponse.data.data)
    })

    it("passes custom page, pageSize, and search params", async () => {
      vi.mocked(apiClient.get).mockResolvedValue(paginatedResponse)

      await varietyService.getAll(2, 25, "gold")

      expect(apiClient.get).toHaveBeenCalledWith("/varieties/", {
        params: { page: 2, page_size: 25, search: "gold" },
      })
    })

    it("passes search as undefined when empty string", async () => {
      vi.mocked(apiClient.get).mockResolvedValue(paginatedResponse)

      await varietyService.getAll(1, 10, "")

      expect(apiClient.get).toHaveBeenCalledWith("/varieties/", {
        params: { page: 1, page_size: 10, search: undefined },
      })
    })
  })

  describe("create", () => {
    it("calls POST /varieties/ with payload", async () => {
      vi.mocked(apiClient.post).mockResolvedValue({ data: {} })

      const payload = { name: "Sun Gold", crop: 1, growthHabit: ["INDETERMINATE"] }

      await varietyService.create(payload)

      expect(apiClient.post).toHaveBeenCalledWith("/varieties/", payload)
    })
  })

  describe("update", () => {
    it("calls PUT /varieties/:id with payload", async () => {
      vi.mocked(apiClient.put).mockResolvedValue({ data: {} })

      const payload = {
        name: "Sun Gold Updated",
        crop: 1,
        growthHabit: ["INDETERMINATE", "DETERMINATE"],
      }

      await varietyService.update(1, payload)

      expect(apiClient.put).toHaveBeenCalledWith("/varieties/1", payload)
    })
  })

  describe("delete", () => {
    it("calls DELETE /varieties/:id", async () => {
      vi.mocked(apiClient.delete).mockResolvedValue({ data: {} })

      await varietyService.delete(1)

      expect(apiClient.delete).toHaveBeenCalledWith("/varieties/1")
    })
  })
})
