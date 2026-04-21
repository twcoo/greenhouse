import { describe, it, expect, vi, beforeEach } from "vitest"
import { setActivePinia, createPinia } from "pinia"
import { useSetupStore } from "@/stores/setupStore"
import axios from "axios"

vi.mock("@/api/services/setupService", () => ({
  getStatus: vi.fn(),
}))

import { getStatus } from "@/api/services/setupService"

beforeEach(() => {
  setActivePinia(createPinia())
  vi.clearAllMocks()
})

describe("setupStore", () => {
  it("sets setupRequired=false and setupChecked=true when getStatus succeeds", async () => {
    vi.mocked(getStatus).mockResolvedValue(undefined)
    const store = useSetupStore()

    await store.checkSetup()

    expect(store.setupRequired).toBe(false)
    expect(store.setupChecked).toBe(true)
    expect(store.backendUnavailable).toBe(false)
  })

  it("sets setupRequired=true when getStatus fails with a server error response", async () => {
    const serverError = new axios.AxiosError("Server Error")
    serverError.response = {
      status: 500,
      data: {},
      headers: {},
      config: {} as never,
      statusText: "Error",
    }
    vi.mocked(getStatus).mockRejectedValue(serverError)
    const store = useSetupStore()

    await store.checkSetup()

    expect(store.setupRequired).toBe(true)
    expect(store.backendUnavailable).toBe(false)
    expect(store.setupChecked).toBe(true)
  })

  it("sets setupRequired=true when getStatus fails with a non-axios error", async () => {
    vi.mocked(getStatus).mockRejectedValue(new Error("unexpected"))
    const store = useSetupStore()

    await store.checkSetup()

    expect(store.setupRequired).toBe(true)
    expect(store.backendUnavailable).toBe(false)
    expect(store.setupChecked).toBe(true)
  })

  it("sets backendUnavailable=true when getStatus fails with no response (network error)", async () => {
    const networkError = new axios.AxiosError("Network Error")
    // no .response property — simulates connection refused
    vi.mocked(getStatus).mockRejectedValue(networkError)
    const store = useSetupStore()

    await store.checkSetup()

    expect(store.backendUnavailable).toBe(true)
    expect(store.setupRequired).toBe(false)
    expect(store.setupChecked).toBe(true)
  })

  it("skips getStatus call if already checked", async () => {
    vi.mocked(getStatus).mockResolvedValue(undefined)
    const store = useSetupStore()
    store.setupChecked = true

    await store.checkSetup()

    expect(getStatus).not.toHaveBeenCalled()
  })

  it("retryConnection resets setupChecked and backendUnavailable", () => {
    const store = useSetupStore()
    store.setupChecked = true
    store.backendUnavailable = true

    store.retryConnection()

    expect(store.setupChecked).toBe(false)
    expect(store.backendUnavailable).toBe(false)
  })
})
