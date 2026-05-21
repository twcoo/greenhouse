import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import { ref } from "vue"
import PlantingLocationsView from "@/views/planting-locations/index.vue"
import PlantingLocationTable from "@/components/planting-locations/PlantingLocationTable.vue"
import PlantingLocationCreateDialog from "@/components/planting-locations/PlantingLocationCreateDialog.vue"
import PlantingLocationUpdateDialog from "@/components/planting-locations/PlantingLocationUpdateDialog.vue"
import PlantingLocationStatusSheet from "@/components/planting-locations/status/PlantingLocationStatusSheet.vue"
import { createTestingPinia } from "@pinia/testing"
import type { PlantingLocation } from "@/types/plantingLocation"

const mockLocations: PlantingLocation[] = [
  { id: 1, name: "Garden Pot", locationType: "POT", width: 30, height: 40 },
  { id: 2, name: "Garden Bed", locationType: "GROUND", width: 100, length: 200 },
]

const mockCreateLocation = vi.fn()
const mockUpdateLocation = vi.fn()
const mockDeleteLocation = vi.fn()
const mockFetchLocations = vi.fn()

vi.mock("@/composables/usePlantingLocations", () => ({
  usePlantingLocations: vi.fn(() => ({
    locations: ref({ results: mockLocations, count: 2 }),
    isLoading: ref(false),
    isCreateSuccess: ref(false),
    isUpdateSuccess: ref(false),
    createLocation: mockCreateLocation,
    updateLocation: mockUpdateLocation,
    deleteLocation: mockDeleteLocation,
    fetchLocations: mockFetchLocations,
  })),
}))

const stubs = {
  AppLayout: { template: "<div><slot /></div>" },
  [PlantingLocationTable.__name ?? "PlantingLocationTable"]: {
    template: "<div data-stub='locations-table' />",
    props: ["data", "rowCount", "pagination", "searchTerm"],
    emits: ["delete", "update", "pagination-change", "update:searchTerm"],
  },
  [PlantingLocationCreateDialog.__name ?? "PlantingLocationCreateDialog"]: {
    template: "<div data-stub='create-dialog' />",
    props: ["open", "isLoading", "isCreateSuccess"],
    emits: ["update:open", "submit"],
  },
  [PlantingLocationUpdateDialog.__name ?? "PlantingLocationUpdateDialog"]: {
    template: "<div data-stub='update-dialog' />",
    props: ["open", "id", "locationFormInitialState", "isLoading", "isUpdateSuccess"],
    emits: ["update:open", "submit"],
  },
  [PlantingLocationStatusSheet.__name ?? "PlantingLocationStatusSheet"]: {
    template: "<div data-stub='status-sheet' />",
    props: ["open", "locationId", "currentStatus"],
    emits: ["update:open"],
  },
  IconLoader2: { template: "<svg />" },
  IconPlus: { template: "<svg />" },
}

const mountComponent = () =>
  mount(PlantingLocationsView, {
    global: {
      plugins: [createTestingPinia({ createSpy: vi.fn })],
      stubs,
    },
  })

beforeEach(() => {
  vi.clearAllMocks()
})

describe("PlantingLocationsView", () => {
  it("renders PlantingLocationTable when locations data is available", () => {
    const wrapper = mountComponent()

    expect(wrapper.find('[data-stub="locations-table"]').exists()).toBe(true)
  })

  it("renders PlantingLocationCreateDialog", () => {
    const wrapper = mountComponent()

    expect(wrapper.find('[data-stub="create-dialog"]').exists()).toBe(true)
  })

  it("opens create dialog when Add Location button is clicked", async () => {
    const wrapper = mountComponent()

    const createDialog = wrapper.findComponent(PlantingLocationCreateDialog)
    expect(createDialog.props("open")).toBe(false)

    await wrapper.find("button").trigger("click")
    await wrapper.vm.$nextTick()

    expect(createDialog.props("open")).toBe(true)
  })

  it("calls deleteLocation with the correct id on delete event from table", async () => {
    const wrapper = mountComponent()

    await wrapper.findComponent(PlantingLocationTable).vm.$emit("delete", 1)

    expect(mockDeleteLocation).toHaveBeenCalledWith(1)
  })

  it("opens update dialog with correct id and form state on update event from table", async () => {
    const wrapper = mountComponent()

    const location = mockLocations[0]
    await wrapper.findComponent(PlantingLocationTable).vm.$emit("update", location.id, {
      name: location.name,
      locationType: location.locationType,
      width: location.width,
      height: location.height,
    })

    await wrapper.vm.$nextTick()

    const updateDialog = wrapper.findComponent(PlantingLocationUpdateDialog)
    expect(updateDialog.props("open")).toBe(true)
    expect(updateDialog.props("id")).toBe(location.id)
  })
})
