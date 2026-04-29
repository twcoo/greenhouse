import { describe, it, expect, vi, beforeEach } from "vitest"

vi.mock("@/api/client", () => ({
  apiClient: {
    get: vi.fn(),
    post: vi.fn(),
  },
}))

import { apiClient } from "@/api/client"
import { plantingLocationStatusService } from "@/api/services/plantingLocationStatusService"

const mockStatus = {
  id: 1,
  status: "AVAILABLE",
  notes: "Ready for use.",
  image: null,
  createdAt: "2024-03-01T00:00:00Z",
}

const paginatedResponse = {
  data: { data: { results: [mockStatus], count: 1, next: null, previous: null } },
}

beforeEach(() => {
  vi.clearAllMocks()
})

describe("plantingLocationStatusService", () => {
  describe("getAll", () => {
    it("calls GET /planting-locations/:id/statuses/ with page_size 100", async () => {
      vi.mocked(apiClient.get).mockResolvedValue(paginatedResponse)

      const result = await plantingLocationStatusService.getAll(1)

      expect(apiClient.get).toHaveBeenCalledWith("/planting-locations/1/statuses/", {
        params: { page_size: 100 },
      })
      expect(result).toEqual(paginatedResponse.data.data)
    })
  })

  describe("create", () => {
    it("calls POST /planting-locations/:id/statuses/ with FormData and multipart header", async () => {
      vi.mocked(apiClient.post).mockResolvedValue({ data: {} })

      await plantingLocationStatusService.create(1, { status: "DAMAGED" })

      expect(apiClient.post).toHaveBeenCalledWith(
        "/planting-locations/1/statuses/",
        expect.any(FormData),
        { headers: { "Content-Type": "multipart/form-data" } },
      )
    })

    it("appends status to FormData", async () => {
      vi.mocked(apiClient.post).mockResolvedValue({ data: {} })

      await plantingLocationStatusService.create(1, { status: "DAMAGED" })

      const formData = vi.mocked(apiClient.post).mock.calls[0][1] as FormData
      expect(formData.get("status")).toBe("DAMAGED")
    })

    it("appends notes when provided", async () => {
      vi.mocked(apiClient.post).mockResolvedValue({ data: {} })

      await plantingLocationStatusService.create(1, { status: "DAMAGED", notes: "Cracked rim." })

      const formData = vi.mocked(apiClient.post).mock.calls[0][1] as FormData
      expect(formData.get("notes")).toBe("Cracked rim.")
    })

    it("does not append notes when absent", async () => {
      vi.mocked(apiClient.post).mockResolvedValue({ data: {} })

      await plantingLocationStatusService.create(1, { status: "DAMAGED" })

      const formData = vi.mocked(apiClient.post).mock.calls[0][1] as FormData
      expect(formData.get("notes")).toBeNull()
    })

    it("appends image when provided", async () => {
      vi.mocked(apiClient.post).mockResolvedValue({ data: {} })

      const file = new File(["content"], "photo.jpg", { type: "image/jpeg" })
      await plantingLocationStatusService.create(1, { status: "DAMAGED", image: file })

      const formData = vi.mocked(apiClient.post).mock.calls[0][1] as FormData
      expect(formData.get("image")).toBe(file)
    })

    it("does not append image when absent", async () => {
      vi.mocked(apiClient.post).mockResolvedValue({ data: {} })

      await plantingLocationStatusService.create(1, { status: "DAMAGED" })

      const formData = vi.mocked(apiClient.post).mock.calls[0][1] as FormData
      expect(formData.get("image")).toBeNull()
    })
  })
})
