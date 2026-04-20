import { describe, it, expect, vi, beforeEach } from "vitest"
import { defineComponent } from "vue"
import { mount, flushPromises } from "@vue/test-utils"
import { VueQueryPlugin, QueryClient } from "@tanstack/vue-query"
import { useVarieties } from "@/composables/useVarieties"

vi.mock("@/api/services/varietyService", () => ({
  varietyService: {
    getAll: vi.fn().mockResolvedValue({ results: [], count: 0 }),
    create: vi.fn().mockResolvedValue(undefined),
    update: vi.fn().mockResolvedValue(undefined),
    delete: vi.fn().mockResolvedValue(undefined),
  },
}))

import { varietyService } from "@/api/services/varietyService"

function mountComposable() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  })

  let result!: ReturnType<typeof useVarieties>

  mount(
    defineComponent({
      setup() {
        result = useVarieties()
        return {}
      },
      template: "<div />",
    }),
    { global: { plugins: [[VueQueryPlugin, { queryClient }]] } },
  )

  return result
}

beforeEach(() => {
  vi.clearAllMocks()
})

const payload = { name: "Sun Gold", crop: 1, growthHabit: ["INDETERMINATE"] }

describe("useVarieties", () => {
  it("returns expected API shape", () => {
    const result = mountComposable()

    expect(result.varieties).toBeDefined()
    expect(result.isLoading).toBeDefined()
    expect(result.isCreateSuccess).toBeDefined()
    expect(result.isUpdateSuccess).toBeDefined()
    expect(typeof result.createVariety).toBe("function")
    expect(typeof result.updateVariety).toBe("function")
    expect(typeof result.deleteVariety).toBe("function")
    expect(typeof result.fetchVarieties).toBe("function")
  })

  it("isLoading is false after query settles with no pending mutations", async () => {
    const result = mountComposable()
    await flushPromises()
    expect(result.isLoading.value).toBe(false)
  })

  it("createVariety calls varietyService.create with the payload", async () => {
    const result = mountComposable()

    await result.createVariety(payload)

    expect(varietyService.create).toHaveBeenCalledWith(payload)
  })

  it("updateVariety calls varietyService.update with id and payload", async () => {
    const result = mountComposable()

    await result.updateVariety({ id: 1, payload })

    expect(varietyService.update).toHaveBeenCalledWith(1, payload)
  })

  it("deleteVariety calls varietyService.delete with id", async () => {
    const result = mountComposable()

    await result.deleteVariety(1)

    expect(varietyService.delete).toHaveBeenCalledWith(1)
  })
})
