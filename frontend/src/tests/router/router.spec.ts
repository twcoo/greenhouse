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
}: { setupRequired?: boolean; isAuthenticated?: boolean } = {}) {
  const setupStore = useSetupStore()
  setupStore.setupChecked = true
  setupStore.setupRequired = setupRequired

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
    // First go somewhere other than /setup so the push below triggers navigation
    await router.push("/login")
    seedStores({ setupRequired: false })

    await router.push("/setup")

    expect(router.currentRoute.value.name).toBe("login")
  })

  it("redirects authenticated user from /login to /dashboard", async () => {
    seedStores({ isAuthenticated: true })

    // Navigate away from /login first so the next push is not a no-op
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

    // Navigate away so /login push is not a no-op
    await router.push("/")
    await router.push("/login")

    expect(router.currentRoute.value.name).toBe("login")
  })
})
