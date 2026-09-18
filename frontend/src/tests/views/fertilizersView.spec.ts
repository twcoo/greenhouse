import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import { ref } from "vue"
import FertilizersView from "@/views/fertilizers/index.vue"
import FertilizersTable from "@/components/fertilizers/FertilizersTable.vue"
import FertilizerCreateDialog from "@/components/fertilizers/FertilizerCreateDialog.vue"
import FertilizerUpdateDialog from "@/components/fertilizers/FertilizerUpdateDialog.vue"
import FertilizerLogSheet from "@/components/fertilizers/logs/FertilizerLogSheet.vue"
import { createTestingPinia } from "@pinia/testing"
import type { Fertilizer } from "@/types/fertilizer"

const mockFertilizers: Fertilizer[] = [
  {
    id: 1,
    name: "Swamp Fertilizer #1",
    type: "SWAMP",
    status: "BREWING",
    startDate: "2024-01-01",
    ingredients: ["banana peels"],
    notes: "",
    createdAt: "2024-01-01T00:00:00Z",
    updatedAt: "2024-01-01T00:00:00Z",
  },
]

const mockCreateFertilizer = vi.fn()
const mockUpdateFertilizer = vi.fn()
const mockDeleteFertilizer = vi.fn()
const mockFetchFertilizers = vi.fn()

vi.mock("@/composables/useFertilizers", () => ({
  useFertilizers: vi.fn(() => ({
    fertilizers: ref({ results: mockFertilizers, count: 1 }),
    isLoading: ref(false),
    isCreateSuccess: ref(false),
    isUpdateSuccess: ref(false),
    createFertilizer: mockCreateFertilizer,
    updateFertilizer: mockUpdateFertilizer,
    deleteFertilizer: mockDeleteFertilizer,
    fetchFertilizers: mockFetchFertilizers,
  })),
}))

const stubs = {
  AppLayout: { template: "<div><slot /></div>" },
  [FertilizersTable.__name ?? "FertilizersTable"]: {
    template: "<div data-stub='fertilizers-table' />",
    props: ["data", "rowCount", "pagination", "searchTerm"],
    emits: ["delete", "update", "action", "pagination-change", "update:searchTerm"],
  },
  [FertilizerCreateDialog.__name ?? "FertilizerCreateDialog"]: {
    template: "<div data-stub='create-dialog' />",
    props: ["open", "isLoading", "isCreateSuccess"],
    emits: ["update:open", "submit"],
  },
  [FertilizerUpdateDialog.__name ?? "FertilizerUpdateDialog"]: {
    template: "<div data-stub='update-dialog' />",
    props: ["open", "id", "fertilizerFormInitialState", "isLoading", "isUpdateSuccess"],
    emits: ["update:open", "submit"],
  },
  [FertilizerLogSheet.__name ?? "FertilizerLogSheet"]: {
    template: "<div data-stub='log-sheet' />",
    props: ["open", "fertilizerId", "fertilizer"],
    emits: ["update:open"],
  },
  IconLoader2: { template: "<svg />" },
  IconPlus: { template: "<svg />" },
}

const mountComponent = () =>
  mount(FertilizersView, {
    global: {
      plugins: [createTestingPinia({ createSpy: vi.fn })],
      stubs,
    },
  })

beforeEach(() => {
  vi.clearAllMocks()
})

describe("FertilizersView", () => {
  it("renders FertilizersTable when data is available", () => {
    const wrapper = mountComponent()

    expect(wrapper.find('[data-stub="fertilizers-table"]').exists()).toBe(true)
  })

  it("renders FertilizerCreateDialog", () => {
    const wrapper = mountComponent()

    expect(wrapper.find('[data-stub="create-dialog"]').exists()).toBe(true)
  })

  it("calls deleteFertilizer on delete event from table", async () => {
    const wrapper = mountComponent()

    await wrapper.findComponent(FertilizersTable).vm.$emit("delete", 1)

    expect(mockDeleteFertilizer).toHaveBeenCalledWith(1)
  })

  it("opens update dialog on update event from table", async () => {
    const wrapper = mountComponent()

    await wrapper.findComponent(FertilizersTable).vm.$emit("update", mockFertilizers[0].id, {
      name: mockFertilizers[0].name,
      type: mockFertilizers[0].type,
      status: mockFertilizers[0].status,
      startDate: mockFertilizers[0].startDate,
      ingredients: mockFertilizers[0].ingredients,
      notes: mockFertilizers[0].notes,
    })

    await wrapper.vm.$nextTick()

    const updateDialog = wrapper.findComponent(FertilizerUpdateDialog)
    expect(updateDialog.props("open")).toBe(true)
    expect(updateDialog.props("id")).toBe(mockFertilizers[0].id)
  })

  it("opens log sheet on manage-logs action from table", async () => {
    const wrapper = mountComponent()

    await wrapper.findComponent(FertilizersTable).vm.$emit("action", "manage-logs", 1)

    await wrapper.vm.$nextTick()

    const logSheet = wrapper.findComponent(FertilizerLogSheet)
    expect(logSheet.exists()).toBe(true)
    expect(logSheet.props("fertilizerId")).toBe(1)
  })
})
