import { describe, it, expect, vi, beforeEach } from "vitest"
import { setActivePinia, createPinia } from "pinia"
import { useAuthStore } from "@/stores/authStore"

vi.mock("@/api/services/authService", () => ({
  authLogin: vi.fn(),
  authLogout: vi.fn(),
}))

vi.mock("@vueuse/integrations/useCookies", () => ({
  useCookies: () => ({ remove: vi.fn() }),
}))

import { authLogin, authLogout } from "@/api/services/authService"

beforeEach(() => {
  localStorage.clear()
  setActivePinia(createPinia())
  vi.clearAllMocks()
})

describe("authStore", () => {
  describe("login", () => {
    it("sets user and isAuthenticated on success", async () => {
      vi.mocked(authLogin).mockResolvedValue({ user: { username: "admin" } })
      const store = useAuthStore()

      await store.login({ username: "admin", password: "pass" })

      expect(store.user).toEqual({ username: "admin" })
      expect(store.isAuthenticated).toBe(true)
      expect(store.isLoading).toBe(false)
      expect(store.error).toBeNull()
    })

    it("sets error message from response on failure with response data", async () => {
      vi.mocked(authLogin).mockRejectedValue({
        response: { data: { message: "Invalid credentials" } },
      })
      const store = useAuthStore()

      await store.login({ username: "admin", password: "wrong" })

      expect(store.isAuthenticated).toBe(false)
      expect(store.user).toBeNull()
      expect(store.error).toBe("Invalid credentials")
      expect(store.isLoading).toBe(false)
    })

    it("sets generic error message on failure without response data", async () => {
      vi.mocked(authLogin).mockRejectedValue({ response: null })
      const store = useAuthStore()

      await store.login({ username: "admin", password: "wrong" })

      expect(store.error).toBe("Something went wrong. Please try again.")
    })
  })

  describe("logout", () => {
    it("clears user and isAuthenticated on success", async () => {
      vi.mocked(authLogout).mockResolvedValue(undefined)
      const store = useAuthStore()
      store.isAuthenticated = true

      await store.logout()

      expect(store.user).toBeNull()
      expect(store.isAuthenticated).toBe(false)
    })

    it("clears user and isAuthenticated even when logout call fails", async () => {
      vi.mocked(authLogout).mockRejectedValue(new Error("Network error"))
      const store = useAuthStore()
      store.isAuthenticated = true

      await store.logout()

      expect(store.user).toBeNull()
      expect(store.isAuthenticated).toBe(false)
    })
  })

  describe("clearAuth", () => {
    it("clears user and isAuthenticated", () => {
      const store = useAuthStore()
      store.isAuthenticated = true

      store.clearAuth()

      expect(store.user).toBeNull()
      expect(store.isAuthenticated).toBe(false)
    })
  })
})
