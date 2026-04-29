import { describe, it, expect, vi, beforeEach } from "vitest"
import { defineComponent, ref } from "vue"
import { mount, flushPromises } from "@vue/test-utils"
import { VueQueryPlugin, QueryClient } from "@tanstack/vue-query"
import { usePlantingLocationStatuses } from "@/composables/usePlantingLocationStatuses"

vi.mock("@/api/services/plantingLocationStatusService", () => ({
  plantingLocationStatusService: {
    getAll: vi.fn().mockResolvedValue({ results: [], count: 0, next: null, previous: null }),
    create: vi.fn().mockResolvedValue(undefined),
  },
}))

import { plantingLocationStatusService } from "@/api/services/plantingLocationStatusService"

function mountComposable(locationId = ref<number | null>(1)) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  })

  let result!: ReturnType<typeof usePlantingLocationStatuses>

  mount(
    defineComponent({
      setup() {
        result = usePlantingLocationStatuses(locationId)
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

describe("usePlantingLocationStatuses", () => {
  it("returns expected API shape", () => {
    const result = mountComposable()

    expect(result.statuses).toBeDefined()
    expect(result.isLoading).toBeDefined()
    expect(result.isQueryError).toBeDefined()
    expect(result.createError).toBeDefined()
    expect(result.isCreateSuccess).toBeDefined()
    expect(typeof result.createStatus).toBe("function")
  })

  it("isLoading is false after query settles with no pending mutations", async () => {
    const result = mountComposable()
    await flushPromises()
    expect(result.isLoading.value).toBe(false)
  })

  it("does not call getAll when locationId is null", async () => {
    mountComposable(ref(null))
    await flushPromises()
    expect(plantingLocationStatusService.getAll).not.toHaveBeenCalled()
  })

  it("createStatus calls plantingLocationStatusService.create with id and payload", async () => {
    const result = mountComposable()
    const payload = { status: "DAMAGED" as const, notes: "Cracked from heat." }

    await result.createStatus({ id: 1, payload })

    expect(plantingLocationStatusService.create).toHaveBeenCalledWith(1, payload)
  })
})
