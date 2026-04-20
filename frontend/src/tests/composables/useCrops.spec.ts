import { describe, it, expect, vi, beforeEach } from "vitest"
import { defineComponent } from "vue"
import { mount, flushPromises } from "@vue/test-utils"
import { VueQueryPlugin, QueryClient } from "@tanstack/vue-query"
import { useCrop } from "@/composables/useCrops"

vi.mock("@/api/services/cropsService", () => ({
  cropService: {
    getAll: vi.fn().mockResolvedValue({ results: [], count: 0 }),
    create: vi.fn().mockResolvedValue(undefined),
    update: vi.fn().mockResolvedValue(undefined),
    delete: vi.fn().mockResolvedValue(undefined),
  },
}))

import { cropService } from "@/api/services/cropsService"

function mountComposable() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  })

  let result!: ReturnType<typeof useCrop>

  mount(
    defineComponent({
      setup() {
        result = useCrop()
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

const payload = {
  name: "Tomato",
  scientificName: "Solanum lycopersicum",
  category: "VEGETABLE",
  sunlightRequirement: "FULL SUN",
  minDaysToHarvest: 60,
  maxDaysToHarvest: 80,
}

describe("useCrop", () => {
  it("returns expected API shape", () => {
    const result = mountComposable()

    expect(result.crops).toBeDefined()
    expect(result.isLoading).toBeDefined()
    expect(result.isCreateSuccess).toBeDefined()
    expect(result.isUpdateSuccess).toBeDefined()
    expect(typeof result.createCrop).toBe("function")
    expect(typeof result.updateCrop).toBe("function")
    expect(typeof result.deleteCrop).toBe("function")
    expect(typeof result.fetchCrops).toBe("function")
  })

  it("isLoading is false after query settles with no pending mutations", async () => {
    const result = mountComposable()
    await flushPromises()
    expect(result.isLoading.value).toBe(false)
  })

  it("createCrop calls cropService.create with the payload", async () => {
    const result = mountComposable()

    await result.createCrop(payload)

    expect(cropService.create).toHaveBeenCalledWith(payload)
  })

  it("updateCrop calls cropService.update with id and payload", async () => {
    const result = mountComposable()

    await result.updateCrop({ id: 1, payload })

    expect(cropService.update).toHaveBeenCalledWith(1, payload)
  })

  it("deleteCrop calls cropService.delete with id", async () => {
    const result = mountComposable()

    await result.deleteCrop(1)

    expect(cropService.delete).toHaveBeenCalledWith(1)
  })
})
