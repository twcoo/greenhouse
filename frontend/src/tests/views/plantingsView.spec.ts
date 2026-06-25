import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import { ref } from "vue"
import PlantingsView from "@/views/plantings/index.vue"
import PlantingsTable from "@/components/plantings/PlantingsTable.vue"
import PlantingCreateDialog from "@/components/plantings/PlantingCreateDialog.vue"
import PlantingUpdateDialog from "@/components/plantings/PlantingUpdateDialog.vue"
import PlantingLocationAssignmentSheet from "@/components/planting-location-assignments/PlantingLocationAssignmentSheet.vue"
import PlantingDailyObservationSheet from "@/components/plantings/daily-observation/PlantingDailyObservationSheet.vue"
import { createTestingPinia } from "@pinia/testing"
import type { Planting } from "@/types/planting"

const mockPlantings: Planting[] = [
  {
    id: 1,
    crop: 1,
    cropName: "Tomato",
    variety: 1,
    varietyName: "Sun Gold",
    status: "ACTIVE",
    currentLocation: null,
    hasDailyObservation: false,
    createdAt: "2024-01-01T00:00:00Z",
  },
  {
    id: 2,
    crop: 1,
    cropName: "Tomato",
    variety: 2,
    varietyName: "Cherokee Purple",
    status: "ACTIVE",
    currentLocation: null,
    hasDailyObservation: false,
    createdAt: "2024-02-01T00:00:00Z",
  },
]

const mockCreatePlanting = vi.fn()
const mockUpdatePlanting = vi.fn()
const mockDeletePlanting = vi.fn()
const mockFetchPlantings = vi.fn()

vi.mock("@/composables/usePlantings", () => ({
  usePlantings: vi.fn(() => ({
    plantings: ref({ results: mockPlantings, count: 2 }),
    isLoading: ref(false),
    isCreateSuccess: ref(false),
    isUpdateSuccess: ref(false),
    createPlanting: mockCreatePlanting,
    updatePlanting: mockUpdatePlanting,
    deletePlanting: mockDeletePlanting,
    fetchPlantings: mockFetchPlantings,
  })),
}))

const stubs = {
  AppLayout: { template: "<div><slot /></div>" },
  [PlantingsTable.__name ?? "PlantingsTable"]: {
    template: "<div data-stub='plantings-table' />",
    props: ["data", "rowCount", "pagination", "searchTerm"],
    emits: ["delete", "update", "pagination-change", "update:searchTerm"],
  },
  [PlantingCreateDialog.__name ?? "PlantingCreateDialog"]: {
    template: "<div data-stub='create-dialog' />",
    props: ["open", "isLoading", "isCreateSuccess"],
    emits: ["update:open", "submit"],
  },
  [PlantingUpdateDialog.__name ?? "PlantingUpdateDialog"]: {
    template: "<div data-stub='update-dialog' />",
    props: ["open", "id", "plantingFormInitialState", "isLoading", "isUpdateSuccess"],
    emits: ["update:open", "submit"],
  },
  [PlantingLocationAssignmentSheet.__name ?? "PlantingLocationAssignmentSheet"]: {
    template: "<div data-stub='location-sheet' :data-open='open' :data-planting-id='plantingId' />",
    props: ["open", "plantingId"],
    emits: ["update:open"],
  },
  [PlantingDailyObservationSheet.__name ?? "PlantingDailyObservationSheet"]: {
    template:
      "<div data-stub='observation-sheet' :data-open='open' :data-planting-id='plantingId' />",
    props: ["open", "plantingId"],
    emits: ["update:open"],
  },
  IconLoader2: { template: "<svg />" },
  IconPlus: { template: "<svg />" },
}

const mountComponent = () =>
  mount(PlantingsView, {
    global: {
      plugins: [createTestingPinia({ createSpy: vi.fn })],
      stubs,
    },
  })

beforeEach(() => {
  vi.clearAllMocks()
})

describe("PlantingsView", () => {
  it("renders PlantingsTable when plantings data is available", () => {
    const wrapper = mountComponent()
    expect(wrapper.find('[data-stub="plantings-table"]').exists()).toBe(true)
  })

  it("renders PlantingCreateDialog", () => {
    const wrapper = mountComponent()
    expect(wrapper.find('[data-stub="create-dialog"]').exists()).toBe(true)
  })

  it("opens create dialog when Add Planting button is clicked", async () => {
    const wrapper = mountComponent()

    const createDialog = wrapper.findComponent(PlantingCreateDialog)
    expect(createDialog.props("open")).toBe(false)

    await wrapper.find("button").trigger("click")
    await wrapper.vm.$nextTick()

    expect(createDialog.props("open")).toBe(true)
  })

  it("calls deletePlanting with the correct id on delete event from table", async () => {
    const wrapper = mountComponent()

    await wrapper.findComponent(PlantingsTable).vm.$emit("delete", 1)

    expect(mockDeletePlanting).toHaveBeenCalledWith(1)
  })

  it("opens update dialog with correct id and form state on update event from table", async () => {
    const wrapper = mountComponent()

    const planting = mockPlantings[0]
    await wrapper.findComponent(PlantingsTable).vm.$emit("update", planting.id, {
      crop: planting.crop,
      variety: planting.variety,
    })

    await wrapper.vm.$nextTick()

    const updateDialog = wrapper.findComponent(PlantingUpdateDialog)
    expect(updateDialog.props("open")).toBe(true)
    expect(updateDialog.props("id")).toBe(planting.id)
  })

  it("opens daily observation sheet with correct plantingId on daily-observations action", async () => {
    const wrapper = mountComponent()

    await wrapper.findComponent(PlantingsTable).vm.$emit("action", "daily-observations", 2)
    await wrapper.vm.$nextTick()

    const sheet = wrapper.find('[data-stub="observation-sheet"]')
    expect(sheet.exists()).toBe(true)
    expect(sheet.attributes("data-open")).toBe("true")
    expect(sheet.attributes("data-planting-id")).toBe("2")
  })

  it("opens location assignment sheet with correct plantingId on manage-locations action", async () => {
    const wrapper = mountComponent()

    await wrapper.findComponent(PlantingsTable).vm.$emit("action", "manage-locations", 1)
    await wrapper.vm.$nextTick()

    const sheet = wrapper.find('[data-stub="location-sheet"]')
    expect(sheet.exists()).toBe(true)
    expect(sheet.attributes("data-open")).toBe("true")
    expect(sheet.attributes("data-planting-id")).toBe("1")
  })
})
