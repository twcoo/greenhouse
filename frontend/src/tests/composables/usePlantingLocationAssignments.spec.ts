import { describe, it, expect, vi, beforeEach } from "vitest"
import { defineComponent, ref } from "vue"
import { mount, flushPromises } from "@vue/test-utils"
import { VueQueryPlugin, QueryClient } from "@tanstack/vue-query"
import { usePlantingLocationAssignments } from "@/composables/usePlantingLocationAssignments"

vi.mock("@/api/services/plantingLocationAssignmentService", () => ({
  plantingLocationAssignmentService: {
    getAll: vi.fn().mockResolvedValue({ results: [], count: 0 }),
    create: vi.fn().mockResolvedValue(undefined),
    update: vi.fn().mockResolvedValue(undefined),
    delete: vi.fn().mockResolvedValue(undefined),
  },
}))

import { plantingLocationAssignmentService } from "@/api/services/plantingLocationAssignmentService"

function mountComposable(plantingId = ref(1)) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  })

  let result!: ReturnType<typeof usePlantingLocationAssignments>

  mount(
    defineComponent({
      setup() {
        result = usePlantingLocationAssignments(plantingId)
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

const payload = { plantingLocation: 2, startDate: "2024-01-01" }

describe("usePlantingLocationAssignments", () => {
  it("returns expected API shape", () => {
    const result = mountComposable()

    expect(result.assignments).toBeDefined()
    expect(result.isLoading).toBeDefined()
    expect(result.isQueryError).toBeDefined()
    expect(result.isCreateSuccess).toBeDefined()
    expect(result.isUpdateSuccess).toBeDefined()
    expect(result.isDeleteSuccess).toBeDefined()
    expect(result.createError).toBeDefined()
    expect(result.updateError).toBeDefined()
    expect(result.deleteError).toBeDefined()
    expect(typeof result.createAssignment).toBe("function")
    expect(typeof result.updateAssignment).toBe("function")
    expect(typeof result.deleteAssignment).toBe("function")
    expect(typeof result.fetchAssignments).toBe("function")
  })

  it("isLoading is false after query settles with no pending mutations", async () => {
    const result = mountComposable()
    await flushPromises()
    expect(result.isLoading.value).toBe(false)
  })

  it("fetches assignments when plantingId is greater than 0", async () => {
    mountComposable(ref(5))
    await flushPromises()

    expect(plantingLocationAssignmentService.getAll).toHaveBeenCalledWith(5)
  })

  it("does not fetch assignments when plantingId is 0", async () => {
    mountComposable(ref(0))
    await flushPromises()

    expect(plantingLocationAssignmentService.getAll).not.toHaveBeenCalled()
  })

  it("createAssignment calls service.create with the plantingId and payload", async () => {
    const result = mountComposable(ref(5))

    await result.createAssignment(payload)

    expect(plantingLocationAssignmentService.create).toHaveBeenCalledWith(5, payload)
  })

  it("updateAssignment calls service.update with plantingId, id, and payload", async () => {
    const result = mountComposable(ref(5))

    await result.updateAssignment({ id: 3, payload })

    expect(plantingLocationAssignmentService.update).toHaveBeenCalledWith(5, 3, payload)
  })

  it("deleteAssignment calls service.delete with plantingId and id", async () => {
    const result = mountComposable(ref(5))

    await result.deleteAssignment(3)

    expect(plantingLocationAssignmentService.delete).toHaveBeenCalledWith(5, 3)
  })
})
