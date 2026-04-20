import { describe, it, expect, vi, beforeEach } from "vitest"
import { setActivePinia, createPinia } from "pinia"
import { useSetupStore } from "@/stores/setupStore"

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
  })

  it("sets setupRequired=true and setupChecked=true when getStatus fails", async () => {
    vi.mocked(getStatus).mockRejectedValue(new Error("Not found"))
    const store = useSetupStore()

    await store.checkSetup()

    expect(store.setupRequired).toBe(true)
    expect(store.setupChecked).toBe(true)
  })

  it("skips getStatus call if already checked", async () => {
    vi.mocked(getStatus).mockResolvedValue(undefined)
    const store = useSetupStore()
    store.setupChecked = true

    await store.checkSetup()

    expect(getStatus).not.toHaveBeenCalled()
  })
})
