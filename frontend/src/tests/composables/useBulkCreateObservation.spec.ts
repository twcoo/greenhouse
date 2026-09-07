import { describe, it, expect, vi, beforeEach } from "vitest"
import { defineComponent } from "vue"
import { mount, flushPromises } from "@vue/test-utils"
import { VueQueryPlugin, QueryClient } from "@tanstack/vue-query"
import { useBulkCreateObservation } from "@/composables/useBulkCreateObservation"

vi.mock("@/api/services/plantingDailyObservationService", () => ({
  plantingDailyObservationService: {
    bulkCreate: vi.fn().mockResolvedValue([]),
  },
}))

import { plantingDailyObservationService } from "@/api/services/plantingDailyObservationService"

function mountComposable() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  })

  let result!: ReturnType<typeof useBulkCreateObservation>

  mount(
    defineComponent({
      setup() {
        result = useBulkCreateObservation()
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

describe("useBulkCreateObservation", () => {
  it("returns expected API shape", () => {
    const { result } = mountComposable()

    expect(typeof result.bulkCreate).toBe("function")
    expect(result.isPending).toBeDefined()
    expect(result.isSuccess).toBeDefined()
  })

  it("isPending is false before any call", () => {
    const { result } = mountComposable()

    expect(result.isPending.value).toBe(false)
  })

  it("calls service.bulkCreate with plantingIds and payload", async () => {
    const { result } = mountComposable()

    await result.bulkCreate({ plantingIds: [1, 2], payload })

    expect(plantingDailyObservationService.bulkCreate).toHaveBeenCalledWith([1, 2], payload)
  })

  it("isSuccess is true after a successful bulk create", async () => {
    const { result } = mountComposable()

    await result.bulkCreate({ plantingIds: [1], payload })
    await flushPromises()

    expect(result.isSuccess.value).toBe(true)
  })

  it("invalidates plantings query on success", async () => {
    const { result, queryClient } = mountComposable()
    const invalidate = vi.spyOn(queryClient, "invalidateQueries")

    await result.bulkCreate({ plantingIds: [1, 2], payload })

    expect(invalidate).toHaveBeenCalledWith({ queryKey: ["plantings"] })
  })
})
