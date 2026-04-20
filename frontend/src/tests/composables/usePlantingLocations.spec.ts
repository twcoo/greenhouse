import { describe, it, expect, vi, beforeEach } from "vitest"
import { defineComponent } from "vue"
import { mount, flushPromises } from "@vue/test-utils"
import { VueQueryPlugin, QueryClient } from "@tanstack/vue-query"
import { usePlantingLocations } from "@/composables/usePlantingLocations"

vi.mock("@/api/services/plantingLocationService", () => ({
  plantingLocationService: {
    getAll: vi.fn().mockResolvedValue({ results: [], count: 0 }),
    create: vi.fn().mockResolvedValue(undefined),
    update: vi.fn().mockResolvedValue(undefined),
    delete: vi.fn().mockResolvedValue(undefined),
    uploadImage: vi.fn().mockResolvedValue(undefined),
  },
}))

import { plantingLocationService } from "@/api/services/plantingLocationService"

function mountComposable() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  })

  let result!: ReturnType<typeof usePlantingLocations>

  mount(
    defineComponent({
      setup() {
        result = usePlantingLocations()
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

const payload = { name: "Garden Pot", locationType: "POT", width: 30, height: 40 }

describe("usePlantingLocations", () => {
  it("returns expected API shape", () => {
    const result = mountComposable()

    expect(result.locations).toBeDefined()
    expect(result.isLoading).toBeDefined()
    expect(result.isCreateSuccess).toBeDefined()
    expect(result.isUpdateSuccess).toBeDefined()
    expect(typeof result.createLocation).toBe("function")
    expect(typeof result.updateLocation).toBe("function")
    expect(typeof result.deleteLocation).toBe("function")
    expect(typeof result.uploadImage).toBe("function")
    expect(typeof result.fetchLocations).toBe("function")
  })

  it("isLoading is false after query settles with no pending mutations", async () => {
    const result = mountComposable()
    await flushPromises()
    expect(result.isLoading.value).toBe(false)
  })

  it("createLocation calls plantingLocationService.create with the payload", async () => {
    const result = mountComposable()

    await result.createLocation(payload)

    expect(plantingLocationService.create).toHaveBeenCalledWith(payload)
  })

  it("updateLocation calls plantingLocationService.update with id and payload", async () => {
    const result = mountComposable()

    await result.updateLocation({ id: 1, payload })

    expect(plantingLocationService.update).toHaveBeenCalledWith(1, payload)
  })

  it("deleteLocation calls plantingLocationService.delete with id", async () => {
    const result = mountComposable()

    await result.deleteLocation(1)

    expect(plantingLocationService.delete).toHaveBeenCalledWith(1)
  })

  it("uploadImage calls plantingLocationService.uploadImage with id and file", async () => {
    const result = mountComposable()
    const file = new File(["content"], "photo.jpg", { type: "image/jpeg" })

    await result.uploadImage({ id: 1, file })

    expect(plantingLocationService.uploadImage).toHaveBeenCalledWith(1, file)
  })
})
