import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import { ref } from "vue"
import VarietiesView from "@/views/varieties/index.vue"
import VarietiesTable from "@/components/varieties/VarietiesTable.vue"
import VarietyCreateDialog from "@/components/varieties/VarietyCreateDialog.vue"
import VarietyUpdateDialog from "@/components/varieties/VarietyUpdateDialog.vue"
import { createTestingPinia } from "@pinia/testing"
import type { Variety } from "@/types/variety"

const mockVarieties: Variety[] = [
  { id: 1, name: "Sun Gold", crop: 1, cropName: "Tomato", growthHabit: ["INDETERMINATE"] },
  { id: 2, name: "Cherokee Purple", crop: 1, cropName: "Tomato", growthHabit: ["DETERMINATE"] },
]

const mockCreateVariety = vi.fn()
const mockUpdateVariety = vi.fn()
const mockDeleteVariety = vi.fn()
const mockFetchVarieties = vi.fn()

vi.mock("@/composables/useVarieties", () => ({
  useVarieties: vi.fn(() => ({
    varieties: ref({ results: mockVarieties, count: 2 }),
    isLoading: ref(false),
    isCreateSuccess: ref(false),
    isUpdateSuccess: ref(false),
    createVariety: mockCreateVariety,
    updateVariety: mockUpdateVariety,
    deleteVariety: mockDeleteVariety,
    fetchVarieties: mockFetchVarieties,
  })),
}))

const stubs = {
  AppLayout: { template: "<div><slot /></div>" },
  [VarietiesTable.__name ?? "VarietiesTable"]: {
    template: "<div data-stub='varieties-table' />",
    props: ["data", "rowCount", "pagination", "searchTerm"],
    emits: ["delete", "update", "pagination-change", "update:searchTerm"],
  },
  [VarietyCreateDialog.__name ?? "VarietyCreateDialog"]: {
    template: "<div data-stub='create-dialog' />",
    props: ["open", "isLoading", "isCreateSuccess"],
    emits: ["update:open", "submit"],
  },
  [VarietyUpdateDialog.__name ?? "VarietyUpdateDialog"]: {
    template: "<div data-stub='update-dialog' />",
    props: ["open", "id", "varietyFormInitialState", "isLoading", "isUpdateSuccess"],
    emits: ["update:open", "submit"],
  },
  IconLoader2: { template: "<svg />" },
  IconPlus: { template: "<svg />" },
}

const mountComponent = () =>
  mount(VarietiesView, {
    global: {
      plugins: [createTestingPinia({ createSpy: vi.fn })],
      stubs,
    },
  })

beforeEach(() => {
  vi.clearAllMocks()
})

describe("VarietiesView", () => {
  it("renders VarietiesTable when varieties data is available", () => {
    const wrapper = mountComponent()

    expect(wrapper.find('[data-stub="varieties-table"]').exists()).toBe(true)
  })

  it("renders VarietyCreateDialog", () => {
    const wrapper = mountComponent()

    expect(wrapper.find('[data-stub="create-dialog"]').exists()).toBe(true)
  })

  it("opens create dialog when Add Variety button is clicked", async () => {
    const wrapper = mountComponent()

    const createDialog = wrapper.findComponent(VarietyCreateDialog)
    expect(createDialog.props("open")).toBe(false)

    await wrapper.find("button").trigger("click")
    await wrapper.vm.$nextTick()

    expect(createDialog.props("open")).toBe(true)
  })

  it("calls deleteVariety with the correct id on delete event from table", async () => {
    const wrapper = mountComponent()

    await wrapper.findComponent(VarietiesTable).vm.$emit("delete", 1)

    expect(mockDeleteVariety).toHaveBeenCalledWith(1)
  })

  it("opens update dialog with correct id and form state on update event from table", async () => {
    const wrapper = mountComponent()

    const variety = mockVarieties[0]
    await wrapper.findComponent(VarietiesTable).vm.$emit("update", variety.id, {
      name: variety.name,
      crop: variety.crop,
      growthHabit: variety.growthHabit,
    })

    await wrapper.vm.$nextTick()

    const updateDialog = wrapper.findComponent(VarietyUpdateDialog)
    expect(updateDialog.props("open")).toBe(true)
    expect(updateDialog.props("id")).toBe(variety.id)
  })
})
