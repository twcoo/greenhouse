import { describe, it, expect, vi, beforeEach } from "vitest"
import { defineComponent } from "vue"
import { mount, flushPromises } from "@vue/test-utils"
import { VueQueryPlugin, QueryClient } from "@tanstack/vue-query"
import { useFertilizers } from "@/composables/useFertilizers"

vi.mock("@/api/services/fertilizerService", () => ({
  fertilizerService: {
    getAll: vi.fn().mockResolvedValue({ results: [], count: 0 }),
    create: vi.fn().mockResolvedValue(undefined),
    update: vi.fn().mockResolvedValue(undefined),
    delete: vi.fn().mockResolvedValue(undefined),
  },
}))

import { fertilizerService } from "@/api/services/fertilizerService"

function mountComposable() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  })

  let result!: ReturnType<typeof useFertilizers>

  mount(
    defineComponent({
      setup() {
        result = useFertilizers()
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

const payload = { name: "Swamp Fertilizer #1", ingredients: ["banana peels"] }

describe("useFertilizers", () => {
  it("returns expected API shape", () => {
    const result = mountComposable()

    expect(result.fertilizers).toBeDefined()
    expect(result.isLoading).toBeDefined()
    expect(result.isCreateSuccess).toBeDefined()
    expect(typeof result.createFertilizer).toBe("function")
    expect(typeof result.updateFertilizer).toBe("function")
    expect(typeof result.deleteFertilizer).toBe("function")
    expect(typeof result.fetchFertilizers).toBe("function")
  })

  it("isLoading is false after query settles with no pending mutations", async () => {
    const result = mountComposable()
    await flushPromises()
    expect(result.isLoading.value).toBe(false)
  })

  it("createFertilizer calls fertilizerService.create with the payload", async () => {
    const result = mountComposable()

    await result.createFertilizer(payload)

    expect(fertilizerService.create).toHaveBeenCalledWith(payload)
  })

  it("updateFertilizer calls fertilizerService.update with id and payload", async () => {
    const result = mountComposable()

    await result.updateFertilizer({ id: 1, payload })

    expect(fertilizerService.update).toHaveBeenCalledWith(1, payload)
  })

  it("deleteFertilizer calls fertilizerService.delete with id", async () => {
    const result = mountComposable()

    await result.deleteFertilizer(1)

    expect(fertilizerService.delete).toHaveBeenCalledWith(1)
  })
})
