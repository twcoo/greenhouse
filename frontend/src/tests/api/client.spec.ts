import { describe, it, expect, vi, beforeEach } from "vitest"
import { setActivePinia, createPinia } from "pinia"

// Mock dependencies before importing client
vi.mock("js-cookie", () => ({
  default: { get: vi.fn() },
}))

vi.mock("@/router", () => ({
  default: {
    currentRoute: { value: { name: "dashboard" } },
    push: vi.fn(),
  },
}))

vi.mock("@/stores/authStore", () => ({
  useAuthStore: vi.fn(() => ({
    clearAuth: vi.fn(),
    error: null,
  })),
}))

import Cookies from "js-cookie"
import router from "@/router"
import { useAuthStore } from "@/stores/authStore"
import { apiClient } from "@/api/client"

beforeEach(() => {
  setActivePinia(createPinia())
  vi.clearAllMocks()
})

// Pull the interceptors out of the axios instance
function getRequestInterceptor() {
  // @ts-expect-error accessing private internals
  const handlers = apiClient.interceptors.request.handlers
  return handlers[handlers.length - 1].fulfilled
}

function getResponseInterceptors() {
  // @ts-expect-error accessing private internals
  const handlers = apiClient.interceptors.response.handlers
  const last = handlers[handlers.length - 1]
  return { onFulfilled: last.fulfilled, onRejected: last.rejected }
}

describe("apiClient request interceptor", () => {
  it("decamelizes request body", () => {
    const interceptor = getRequestInterceptor()
    const config = { data: { growthHabit: ["INDETERMINATE"], minDays: 60 }, headers: {} }

    const result = interceptor(config)

    expect(result.data).toEqual({ growth_habit: ["INDETERMINATE"], min_days: 60 })
  })

  it("does not modify config when data is absent", () => {
    const interceptor = getRequestInterceptor()
    const config = { headers: {} }

    const result = interceptor(config)

    expect(result.data).toBeUndefined()
  })

  it("injects X-CSRFToken when cookie is present", () => {
    vi.mocked(Cookies.get).mockReturnValue("csrf-abc")
    const interceptor = getRequestInterceptor()
    const config = { headers: {} }

    const result = interceptor(config)

    expect(result.headers["X-CSRFToken"]).toBe("csrf-abc")
  })

  it("does not add X-CSRFToken when cookie is absent", () => {
    vi.mocked(Cookies.get).mockReturnValue(undefined)
    const interceptor = getRequestInterceptor()
    const config = { headers: {} }

    const result = interceptor(config)

    expect(result.headers["X-CSRFToken"]).toBeUndefined()
  })
})

describe("apiClient response interceptor", () => {
  describe("success handler", () => {
    it("camelizes response data", () => {
      const { onFulfilled } = getResponseInterceptors()
      const response = { data: { growth_habit: ["INDETERMINATE"], min_days: 60 } }

      const result = onFulfilled(response)

      expect(result.data).toEqual({ growthHabit: ["INDETERMINATE"], minDays: 60 })
    })

    it("returns response unchanged when data is absent", () => {
      const { onFulfilled } = getResponseInterceptors()
      const response = { status: 204 }

      const result = onFulfilled(response)

      expect(result).toEqual({ status: 204 })
    })
  })

  describe("error handler", () => {
    it("camelizes error response data", async () => {
      const { onRejected } = getResponseInterceptors()
      const error = {
        response: { status: 400, data: { field_name: ["This field is required."] } },
      }

      await expect(onRejected(error)).rejects.toEqual(error)
      expect(error.response.data).toEqual({ fieldName: ["This field is required."] })
    })

    it("redirects to login and clears auth on 401 when not on login page", async () => {
      const mockAuthStore = { clearAuth: vi.fn(), error: null as string | null }
      vi.mocked(useAuthStore).mockReturnValue(mockAuthStore as ReturnType<typeof useAuthStore>)
      vi.mocked(router.currentRoute).value.name = "dashboard"

      const { onRejected } = getResponseInterceptors()
      const error = { response: { status: 401, data: null } }

      await expect(onRejected(error)).rejects.toEqual(error)

      expect(mockAuthStore.clearAuth).toHaveBeenCalled()
      expect(mockAuthStore.error).toBe("Your session has expired. Please login again.")
      expect(router.push).toHaveBeenCalledWith({
        name: "login",
        query: { redirectTo: "dashboard" },
      })
    })

    it("redirects to login and clears auth on 403 when not on login page", async () => {
      const mockAuthStore = { clearAuth: vi.fn(), error: null as string | null }
      vi.mocked(useAuthStore).mockReturnValue(mockAuthStore as ReturnType<typeof useAuthStore>)
      vi.mocked(router.currentRoute).value.name = "crops"

      const { onRejected } = getResponseInterceptors()
      const error = { response: { status: 403, data: null } }

      await expect(onRejected(error)).rejects.toEqual(error)

      expect(mockAuthStore.clearAuth).toHaveBeenCalled()
      expect(router.push).toHaveBeenCalledWith({
        name: "login",
        query: { redirectTo: "crops" },
      })
    })

    it("does not redirect when already on login page", async () => {
      vi.mocked(router.currentRoute).value.name = "login"

      const { onRejected } = getResponseInterceptors()
      const error = { response: { status: 401, data: null } }

      await expect(onRejected(error)).rejects.toEqual(error)

      expect(router.push).not.toHaveBeenCalled()
    })

    it("does not redirect on non-auth errors", async () => {
      vi.mocked(router.currentRoute).value.name = "dashboard"

      const { onRejected } = getResponseInterceptors()
      const error = { response: { status: 500, data: null } }

      await expect(onRejected(error)).rejects.toEqual(error)

      expect(router.push).not.toHaveBeenCalled()
    })

    it("handles errors with no response object", async () => {
      const { onRejected } = getResponseInterceptors()
      const error = new Error("Network Error")

      await expect(onRejected(error)).rejects.toEqual(error)

      expect(router.push).not.toHaveBeenCalled()
    })
  })
})
