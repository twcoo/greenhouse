import { describe, it, expect, vi, beforeEach } from "vitest"

vi.mock("@/api/client", () => ({
  apiClient: {
    post: vi.fn(),
  },
}))

import { apiClient } from "@/api/client"
import { authLogin, authLogout } from "@/api/services/authService"

beforeEach(() => {
  vi.clearAllMocks()
})

describe("authService", () => {
  describe("authLogin", () => {
    it("calls POST auth/login with payload and returns data", async () => {
      const mockData = { token: "abc123" }
      vi.mocked(apiClient.post).mockResolvedValue({ data: { data: mockData } })

      const result = await authLogin({ username: "admin", password: "secret" })

      expect(apiClient.post).toHaveBeenCalledWith("auth/login", {
        username: "admin",
        password: "secret",
      })
      expect(result).toEqual(mockData)
    })
  })

  describe("authLogout", () => {
    it("calls POST auth/logout", async () => {
      vi.mocked(apiClient.post).mockResolvedValue({ data: {} })

      await authLogout()

      expect(apiClient.post).toHaveBeenCalledWith("auth/logout")
    })
  })
})
