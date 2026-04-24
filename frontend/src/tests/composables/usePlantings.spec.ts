import { describe, it, expect, vi, beforeEach } from "vitest"
import { defineComponent } from "vue"
import { mount, flushPromises } from "@vue/test-utils"
import { VueQueryPlugin, QueryClient } from "@tanstack/vue-query"
import { usePlantings } from "@/composables/usePlantings"

vi.mock("@/api/services/plantingService", () => ({
  plantingService: {
    getAll: vi.fn().mockResolvedValue({ results: [], count: 0 }),
    create: vi.fn().mockResolvedValue(undefined),
    update: vi.fn().mockResolvedValue(undefined),
    delete: vi.fn().mockResolvedValue(undefined),
  },
}))

import { plantingService } from "@/api/services/plantingService"

function mountComposable() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  })

  let result!: ReturnType<typeof usePlantings>

  mount(
    defineComponent({
      setup() {
        result = usePlantings()
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

const payload = { crop: 1, variety: 1 }

describe("usePlantings", () => {
  it("returns expected API shape", () => {
    const result = mountComposable()

    expect(result.plantings).toBeDefined()
    expect(result.isLoading).toBeDefined()
    expect(result.isCreateSuccess).toBeDefined()
    expect(result.isUpdateSuccess).toBeDefined()
    expect(typeof result.createPlanting).toBe("function")
    expect(typeof result.updatePlanting).toBe("function")
    expect(typeof result.deletePlanting).toBe("function")
    expect(typeof result.fetchPlantings).toBe("function")
  })

  it("isLoading is false after query settles with no pending mutations", async () => {
    const result = mountComposable()
    await flushPromises()
    expect(result.isLoading.value).toBe(false)
  })

  it("createPlanting calls plantingService.create with the payload", async () => {
    const result = mountComposable()

    await result.createPlanting(payload)

    expect(plantingService.create).toHaveBeenCalledWith(payload)
  })

  it("updatePlanting calls plantingService.update with id and payload", async () => {
    const result = mountComposable()

    await result.updatePlanting({ id: 1, payload })

    expect(plantingService.update).toHaveBeenCalledWith(1, payload)
  })

  it("deletePlanting calls plantingService.delete with id", async () => {
    const result = mountComposable()

    await result.deletePlanting(1)

    expect(plantingService.delete).toHaveBeenCalledWith(1)
  })
})
