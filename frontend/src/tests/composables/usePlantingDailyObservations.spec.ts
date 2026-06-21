import { describe, it, expect, vi, beforeEach } from "vitest"
import { defineComponent, ref } from "vue"
import { mount, flushPromises } from "@vue/test-utils"
import { VueQueryPlugin, QueryClient } from "@tanstack/vue-query"
import { usePlantingDailyObservations } from "@/composables/usePlantingDailyObservations"

vi.mock("@/api/services/plantingDailyObservationService", () => ({
  plantingDailyObservationService: {
    getAll: vi.fn().mockResolvedValue({ results: [], count: 0 }),
    create: vi.fn().mockResolvedValue(undefined),
    update: vi.fn().mockResolvedValue(undefined),
    delete: vi.fn().mockResolvedValue(undefined),
  },
}))

import { plantingDailyObservationService } from "@/api/services/plantingDailyObservationService"

function mountComposable(plantingId = ref(1)) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  })

  let result!: ReturnType<typeof usePlantingDailyObservations>

  mount(
    defineComponent({
      setup() {
        result = usePlantingDailyObservations(plantingId)
        return {}
      },
      template: "<div />",
    }),
    { global: { plugins: [[VueQueryPlugin, { queryClient }]] } },
  )

  return { result, queryClient }
}

beforeEach(() => {
  vi.clearAllMocks()
})

const payload = {
  healthStatus: "GOOD" as const,
  pestPressure: "NONE" as const,
  diseaseSymptoms: false,
}

describe("usePlantingDailyObservations", () => {
  it("returns expected API shape", () => {
    const { result } = mountComposable()

    expect(result.observations).toBeDefined()
    expect(result.isLoading).toBeDefined()
    expect(result.isQueryError).toBeDefined()
    expect(result.isCreateSuccess).toBeDefined()
    expect(result.isUpdateSuccess).toBeDefined()
    expect(result.isDeleteSuccess).toBeDefined()
    expect(result.createError).toBeDefined()
    expect(result.updateError).toBeDefined()
    expect(result.deleteError).toBeDefined()
    expect(typeof result.createObservation).toBe("function")
    expect(typeof result.updateObservation).toBe("function")
    expect(typeof result.deleteObservation).toBe("function")
    expect(typeof result.fetchObservations).toBe("function")
  })

  it("isLoading is false after query settles with no pending mutations", async () => {
    const { result } = mountComposable()
    await flushPromises()

    expect(result.isLoading.value).toBe(false)
  })

  it("fetches observations when plantingId is greater than 0", async () => {
    mountComposable(ref(5))
    await flushPromises()

    expect(plantingDailyObservationService.getAll).toHaveBeenCalledWith(5, 1, 10)
  })

  it("does not fetch observations when plantingId is 0", async () => {
    mountComposable(ref(0))
    await flushPromises()

    expect(plantingDailyObservationService.getAll).not.toHaveBeenCalled()
  })

  it("createObservation calls service.create with the plantingId and payload", async () => {
    const { result } = mountComposable(ref(5))

    await result.createObservation(payload)

    expect(plantingDailyObservationService.create).toHaveBeenCalledWith(5, payload)
  })

  it("updateObservation calls service.update with plantingId, id, and payload", async () => {
    const { result } = mountComposable(ref(5))

    await result.updateObservation({ id: 3, payload })

    expect(plantingDailyObservationService.update).toHaveBeenCalledWith(5, 3, payload)
  })

  it("deleteObservation calls service.delete with plantingId and id", async () => {
    const { result } = mountComposable(ref(5))

    await result.deleteObservation(3)

    expect(plantingDailyObservationService.delete).toHaveBeenCalledWith(5, 3)
  })

  it("isCreateSuccess is true after a successful create", async () => {
    const { result } = mountComposable(ref(5))

    await result.createObservation(payload)
    await flushPromises()

    expect(result.isCreateSuccess.value).toBe(true)
  })

  it("isUpdateSuccess is true after a successful update", async () => {
    const { result } = mountComposable(ref(5))

    await result.updateObservation({ id: 3, payload })
    await flushPromises()

    expect(result.isUpdateSuccess.value).toBe(true)
  })

  it("isDeleteSuccess is true after a successful delete", async () => {
    const { result } = mountComposable(ref(5))

    await result.deleteObservation(3)
    await flushPromises()

    expect(result.isDeleteSuccess.value).toBe(true)
  })

  it("createObservation invalidates the plantings query", async () => {
    const { result, queryClient } = mountComposable(ref(5))
    const invalidate = vi.spyOn(queryClient, "invalidateQueries")

    await result.createObservation(payload)

    expect(invalidate).toHaveBeenCalledWith({ queryKey: ["plantings"] })
  })
})
