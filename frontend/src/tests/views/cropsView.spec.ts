import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import { ref } from "vue"
import CropsView from "@/views/crops/index.vue"
import CropsTable from "@/components/crops/CropsTable.vue"
import CropCreateDialog from "@/components/crops/CropCreateDialog.vue"
import CropUpdateDialog from "@/components/crops/CropUpdateDialog.vue"
import { createTestingPinia } from "@pinia/testing"
import type { Crop } from "@/types/crop"

const mockCrops: Crop[] = [
  {
    id: 1,
    name: "Tomato",
    scientificName: "Solanum lycopersicum",
    category: "VEGETABLE",
    sunlightRequirement: "FULL SUN",
    minDaysToHarvest: 60,
    maxDaysToHarvest: 80,
  },
  {
    id: 2,
    name: "Pepper",
    scientificName: "Capsicum annuum",
    category: "VEGETABLE",
    sunlightRequirement: "FULL SUN",
    minDaysToHarvest: 70,
    maxDaysToHarvest: 90,
  },
]

const mockCreateCrop = vi.fn()
const mockUpdateCrop = vi.fn()
const mockDeleteCrop = vi.fn()
const mockFetchCrops = vi.fn()

vi.mock("@/composables/useCrops", () => ({
  useCrop: vi.fn(() => ({
    crops: ref({ results: mockCrops, count: 2 }),
    isLoading: ref(false),
    isCreateSuccess: ref(false),
    isUpdateSuccess: ref(false),
    createCrop: mockCreateCrop,
    updateCrop: mockUpdateCrop,
    deleteCrop: mockDeleteCrop,
    fetchCrops: mockFetchCrops,
  })),
}))

const stubs = {
  AppLayout: { template: "<div><slot /></div>" },
  [CropsTable.__name ?? "CropsTable"]: {
    template: "<div data-stub='crops-table' />",
    props: ["data", "rowCount", "pagination", "searchTerm"],
    emits: ["delete", "update", "pagination-change", "update:searchTerm"],
  },
  [CropCreateDialog.__name ?? "CropCreateDialog"]: {
    template: "<div data-stub='create-dialog' />",
    props: ["open", "isLoading", "isCreateSuccess"],
    emits: ["update:open", "submit"],
  },
  [CropUpdateDialog.__name ?? "CropUpdateDialog"]: {
    template: "<div data-stub='update-dialog' />",
    props: ["open", "id", "cropsFormInitialState", "isLoading", "isUpdateSuccess", "searchTerm"],
    emits: ["update:open", "submit", "update:searchTerm"],
  },
  IconLoader2: { template: "<svg />" },
  IconPlus: { template: "<svg />" },
}

const mountComponent = () =>
  mount(CropsView, {
    global: {
      plugins: [createTestingPinia({ createSpy: vi.fn })],
      stubs,
    },
  })

beforeEach(() => {
  vi.clearAllMocks()
})

describe("CropsView", () => {
  it("renders CropsTable when crops data is available", () => {
    const wrapper = mountComponent()

    expect(wrapper.find('[data-stub="crops-table"]').exists()).toBe(true)
  })

  it("renders CropCreateDialog", () => {
    const wrapper = mountComponent()

    expect(wrapper.find('[data-stub="create-dialog"]').exists()).toBe(true)
  })

  it("opens create dialog when Add Crop button is clicked", async () => {
    const wrapper = mountComponent()

    const createDialog = wrapper.findComponent(CropCreateDialog)
    expect(createDialog.props("open")).toBe(false)

    await wrapper.find("button").trigger("click")
    await wrapper.vm.$nextTick()

    expect(createDialog.props("open")).toBe(true)
  })

  it("calls deleteCrop with the correct id on delete event from table", async () => {
    const wrapper = mountComponent()

    await wrapper.findComponent(CropsTable).vm.$emit("delete", 1)

    expect(mockDeleteCrop).toHaveBeenCalledWith(1)
  })

  it("opens update dialog with correct id and form state on update event from table", async () => {
    const wrapper = mountComponent()

    const crop = mockCrops[0]
    await wrapper.findComponent(CropsTable).vm.$emit("update", crop.id, {
      name: crop.name,
      scientificName: crop.scientificName,
      category: crop.category,
      sunlightRequirement: crop.sunlightRequirement,
      minDaysToHarvest: crop.minDaysToHarvest,
      maxDaysToHarvest: crop.maxDaysToHarvest,
    })

    await wrapper.vm.$nextTick()

    const updateDialog = wrapper.findComponent(CropUpdateDialog)
    expect(updateDialog.props("open")).toBe(true)
    expect(updateDialog.props("id")).toBe(crop.id)
  })
})
