import { describe, it, expect, vi, beforeEach } from "vitest"
import { setActivePinia, createPinia } from "pinia"
import { useSetupStore } from "@/stores/setupStore"
import { useAuthStore } from "@/stores/authStore"
import router from "@/router/index"

vi.mock("@/api/services/setupService", () => ({
  getStatus: vi.fn().mockResolvedValue(undefined),
  createAdmin: vi.fn(),
}))

vi.mock("@/api/services/authService", () => ({
  authLogin: vi.fn(),
  authLogout: vi.fn(),
}))

vi.mock("@vueuse/integrations/useCookies", () => ({
  useCookies: () => ({ remove: vi.fn() }),
}))

// Seed store state and return refs for use in tests
function seedStores({
  setupRequired = false,
  isAuthenticated = false,
  backendUnavailable = false,
}: { setupRequired?: boolean; isAuthenticated?: boolean; backendUnavailable?: boolean } = {}) {
  const setupStore = useSetupStore()
  setupStore.setupChecked = true
  setupStore.setupRequired = setupRequired
  setupStore.backendUnavailable = backendUnavailable

  const authStore = useAuthStore()
  authStore.isAuthenticated = isAuthenticated

  return { setupStore, authStore }
}

beforeEach(async () => {
  localStorage.clear()
  setActivePinia(createPinia())
  vi.clearAllMocks()

  // Bring router to a stable base: setup complete, not authenticated, at /login
  seedStores()
  // Avoid no-op if already at /login by going somewhere neutral first
  await router.push("/")
  await router.push("/login")
})

describe("router beforeEach guard", () => {
  it("redirects to /setup when setup is required and navigating to protected route", async () => {
    seedStores({ setupRequired: true })

    await router.push("/dashboard")

    expect(router.currentRoute.value.name).toBe("setup")
  })

  it("redirects away from /setup to /login when setup is already complete", async () => {
    await router.push("/login")
    seedStores({ setupRequired: false })

    await router.push("/setup")

    expect(router.currentRoute.value.name).toBe("login")
  })

  it("redirects authenticated user from /login to /dashboard", async () => {
    seedStores({ isAuthenticated: true })

    await router.push("/crops")
    await router.push("/login")

    expect(router.currentRoute.value.name).toBe("dashboard")
  })

  it("redirects unauthenticated user from protected route to /login", async () => {
    seedStores({ isAuthenticated: false })

    await router.push("/crops")

    expect(router.currentRoute.value.name).toBe("login")
  })

  it("allows authenticated user to access a protected route", async () => {
    seedStores({ isAuthenticated: true })

    await router.push("/crops")

    expect(router.currentRoute.value.name).toBe("crops")
  })

  it("allows unauthenticated user to access /login", async () => {
    seedStores({ isAuthenticated: false })

    await router.push("/")
    await router.push("/login")

    expect(router.currentRoute.value.name).toBe("login")
  })

  describe("service-unavailable route", () => {
    it("redirects to /service-unavailable when backend is unreachable", async () => {
      seedStores({ backendUnavailable: true })

      await router.push("/dashboard")

      expect(router.currentRoute.value.name).toBe("service-unavailable")
    })

    it("redirects to /service-unavailable even when navigating to /login", async () => {
      // Navigate to a non-login route first so the /login push is not a no-op
      seedStores({ isAuthenticated: true })
      await router.push("/dashboard")

      seedStores({ backendUnavailable: true })
      await router.push("/login")

      expect(router.currentRoute.value.name).toBe("service-unavailable")
    })

    it("redirects away from /service-unavailable to /login when backend becomes reachable and user is unauthenticated", async () => {
      seedStores({ backendUnavailable: false, isAuthenticated: false })

      await router.push("/")
      await router.push("/service-unavailable")

      expect(router.currentRoute.value.name).toBe("login")
    })

    it("redirects away from /service-unavailable to /dashboard when backend becomes reachable and user is authenticated", async () => {
      seedStores({ backendUnavailable: false, isAuthenticated: true })

      await router.push("/crops")
      await router.push("/service-unavailable")

      expect(router.currentRoute.value.name).toBe("dashboard")
    })

    it("allows access to /service-unavailable when backend is unavailable", async () => {
      seedStores({ backendUnavailable: true })

      await router.push("/service-unavailable")

      expect(router.currentRoute.value.name).toBe("service-unavailable")
    })
  })
})
