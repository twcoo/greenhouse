import { describe, it, expect, vi, beforeEach } from "vitest"
import { defineComponent, ref } from "vue"
import { mount, flushPromises } from "@vue/test-utils"
import { VueQueryPlugin, QueryClient } from "@tanstack/vue-query"
import { useFertilizerLogs } from "@/composables/useFertilizerLogs"

vi.mock("@/api/services/fertilizerLogService", () => ({
  fertilizerLogService: {
    getAll: vi.fn().mockResolvedValue({ results: [], count: 0 }),
    create: vi.fn().mockResolvedValue(undefined),
    update: vi.fn().mockResolvedValue(undefined),
    delete: vi.fn().mockResolvedValue(undefined),
  },
}))

import { fertilizerLogService } from "@/api/services/fertilizerLogService"

function mountComposable(fertilizerId = 5) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  })

  let result!: ReturnType<typeof useFertilizerLogs>

  mount(
    defineComponent({
      setup() {
        result = useFertilizerLogs(ref(fertilizerId))
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

const payload = { eventType: "ADDED_WATER", quantity: "5 liters" }

describe("useFertilizerLogs", () => {
  it("returns expected API shape", () => {
    const { result } = mountComposable()

    expect(result.logs).toBeDefined()
    expect(result.isLoading).toBeDefined()
    expect(result.isCreateSuccess).toBeDefined()
    expect(typeof result.createLog).toBe("function")
    expect(typeof result.updateLog).toBe("function")
    expect(typeof result.deleteLog).toBe("function")
    expect(typeof result.fetchLogs).toBe("function")
  })

  it("isLoading is false after query settles", async () => {
    const { result } = mountComposable()
    await flushPromises()
    expect(result.isLoading.value).toBe(false)
  })

  it("createLog calls fertilizerLogService.create with id and payload", async () => {
    const { result } = mountComposable()

    await result.createLog(payload)

    expect(fertilizerLogService.create).toHaveBeenCalledWith(5, payload)
  })

  it("updateLog calls fertilizerLogService.update with id, log id, and payload", async () => {
    const { result } = mountComposable()

    await result.updateLog({ id: 1, payload })

    expect(fertilizerLogService.update).toHaveBeenCalledWith(5, 1, payload)
  })

  it("deleteLog calls fertilizerLogService.delete with id and log id", async () => {
    const { result } = mountComposable()

    await result.deleteLog(1)

    expect(fertilizerLogService.delete).toHaveBeenCalledWith(5, 1)
  })

  it("createLog invalidates the fertilizers query", async () => {
    const { result, queryClient } = mountComposable()
    const invalidate = vi.spyOn(queryClient, "invalidateQueries")

    await result.createLog(payload)

    expect(invalidate).toHaveBeenCalledWith({ queryKey: ["fertilizers"] })
  })

  it("updateLog invalidates the fertilizers query", async () => {
    const { result, queryClient } = mountComposable()
    const invalidate = vi.spyOn(queryClient, "invalidateQueries")

    await result.updateLog({ id: 1, payload })

    expect(invalidate).toHaveBeenCalledWith({ queryKey: ["fertilizers"] })
  })

  it("deleteLog invalidates the fertilizers query", async () => {
    const { result, queryClient } = mountComposable()
    const invalidate = vi.spyOn(queryClient, "invalidateQueries")

    await result.deleteLog(1)

    expect(invalidate).toHaveBeenCalledWith({ queryKey: ["fertilizers"] })
  })
})
