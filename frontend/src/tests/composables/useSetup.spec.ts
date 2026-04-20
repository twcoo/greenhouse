import { describe, it, expect, vi, beforeEach } from "vitest"
import { defineComponent } from "vue"
import { mount } from "@vue/test-utils"
import { useSetup } from "@/composables/useSetup"

vi.mock("@/api/services/setupService", () => ({
  createAdmin: vi.fn(),
  getStatus: vi.fn(),
}))

import { createAdmin } from "@/api/services/setupService"

function mountComposable() {
  let result!: ReturnType<typeof useSetup>

  mount(
    defineComponent({
      setup() {
        result = useSetup()
        return {}
      },
      template: "<div />",
    }),
  )

  return result
}

beforeEach(() => {
  vi.clearAllMocks()
})

describe("useSetup", () => {
  it("returns loading ref and setupAdmin function", () => {
    const result = mountComposable()

    expect(result.loading).toBeDefined()
    expect(result.loading.value).toBe(false)
    expect(typeof result.setupAdmin).toBe("function")
  })

  it("setupAdmin calls createAdmin and returns data on success", async () => {
    const mockResponse = { token: "abc123" }
    vi.mocked(createAdmin).mockResolvedValue(mockResponse as never)
    const result = mountComposable()
    const payload = { username: "admin", password: "pass", password2: "pass", email: "a@b.com" }

    const data = await result.setupAdmin(payload)

    expect(createAdmin).toHaveBeenCalledWith(payload)
    expect(data).toEqual(mockResponse)
    expect(result.loading.value).toBe(false)
  })

  it("setupAdmin re-throws when createAdmin fails", async () => {
    vi.mocked(createAdmin).mockRejectedValue(new Error("Setup failed"))
    const result = mountComposable()
    const payload = { username: "admin", password: "pass", password2: "pass", email: "a@b.com" }

    await expect(result.setupAdmin(payload)).rejects.toThrow("Setup failed")
    expect(result.loading.value).toBe(false)
  })
})
