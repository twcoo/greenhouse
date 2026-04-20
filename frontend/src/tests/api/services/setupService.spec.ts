import { describe, it, expect, vi, beforeEach } from "vitest"

vi.mock("@/api/client", () => ({
  apiClient: {
    get: vi.fn(),
    post: vi.fn(),
  },
}))

import { apiClient } from "@/api/client"
import { createAdmin, getStatus } from "@/api/services/setupService"

beforeEach(() => {
  vi.clearAllMocks()
})

describe("setupService", () => {
  describe("createAdmin", () => {
    it("calls POST setup/admin with payload and returns data", async () => {
      const mockResponse = { id: 1, username: "admin" }
      vi.mocked(apiClient.post).mockResolvedValue({ data: { data: mockResponse } })

      const payload = { username: "admin", password: "secret", email: "admin@example.com" }
      const result = await createAdmin(payload)

      expect(apiClient.post).toHaveBeenCalledWith("setup/admin", payload)
      expect(result).toEqual(mockResponse)
    })
  })

  describe("getStatus", () => {
    it("calls GET /setup/status", async () => {
      vi.mocked(apiClient.get).mockResolvedValue({ data: {} })

      await getStatus()

      expect(apiClient.get).toHaveBeenCalledWith("/setup/status")
    })
  })
})
