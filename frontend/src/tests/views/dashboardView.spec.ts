import { ref } from "vue"
import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import DashboardView from "@/views/dashboard/index.vue"
import { createTestingPinia } from "@pinia/testing"

vi.mock("@/composables/usePlantings", () => ({
  usePlantings: vi.fn(),
}))
vi.mock("@/composables/usePlantingLocations", () => ({
  usePlantingLocations: vi.fn(),
}))

import { usePlantings } from "@/composables/usePlantings"
import { usePlantingLocations } from "@/composables/usePlantingLocations"

const defaultPlantings = [
  {
    id: 1,
    crop: 1,
    cropName: "Tomato",
    variety: 1,
    varietyName: "Sun Gold",
    createdAt: "2024-01-01T00:00:00Z",
  },
  {
    id: 2,
    crop: 2,
    cropName: "Basil",
    variety: 2,
    varietyName: "Genovese",
    createdAt: "2024-03-01T00:00:00Z",
  },
  {
    id: 3,
    crop: 3,
    cropName: "Pepper",
    variety: 3,
    varietyName: "Bell",
    createdAt: "2024-02-01T00:00:00Z",
  },
]

const defaultLocations = [
  {
    id: 1,
    name: "Balcony Pot",
    locationType: "POT",
    width: 25,
    currentStatus: { id: 1, status: "IN_USE", notes: "", createdAt: "2024-03-01T00:00:00Z" },
  },
  {
    id: 2,
    name: "Nursery A",
    locationType: "NURSERYPOT",
    width: 15,
    currentStatus: { id: 2, status: "AVAILABLE", notes: "", createdAt: "2024-03-01T00:00:00Z" },
  },
  {
    id: 3,
    name: "Garden Bed",
    locationType: "GROUND",
    width: 100,
    currentStatus: null,
  },
]

function setupMock(
  plantingOverrides: Record<string, unknown> = {},
  locationOverrides: Record<string, unknown> = {},
) {
  vi.mocked(usePlantings).mockReturnValue({
    plantings: ref({ results: defaultPlantings, count: defaultPlantings.length }),
    isLoading: ref(false),
    isQueryError: ref(false),
    createError: ref(false),
    updateError: ref(false),
    deleteError: ref(false),
    isCreateSuccess: ref(false),
    isUpdateSuccess: ref(false),
    isDeleteSuccess: ref(false),
    createPlanting: vi.fn(),
    updatePlanting: vi.fn(),
    deletePlanting: vi.fn(),
    fetchPlantings: vi.fn(),
    ...plantingOverrides,
  })

  vi.mocked(usePlantingLocations).mockReturnValue({
    locations: ref({ results: defaultLocations, count: defaultLocations.length }),
    isLoading: ref(false),
    isQueryError: ref(false),
    createError: ref(false),
    updateError: ref(false),
    deleteError: ref(false),
    isCreateSuccess: ref(false),
    isUpdateSuccess: ref(false),
    isDeleteSuccess: ref(false),
    createLocation: vi.fn(),
    updateLocation: vi.fn(),
    deleteLocation: vi.fn(),
    fetchLocations: vi.fn(),
    ...locationOverrides,
  })
}

const stubs = {
  AppLayout: { template: "<div><slot /></div>" },
  Card: { template: "<div><slot /></div>" },
  CardHeader: { template: "<div><slot /></div>" },
  CardContent: { template: "<div><slot /></div>" },
  CardTitle: { template: "<p data-test='card-title'><slot /></p>" },
  CardDescription: { template: "<p><slot /></p>" },
  Badge: { template: "<span data-test='badge'><slot /></span>" },
  Table: { template: "<table><slot /></table>" },
  TableHeader: { template: "<thead><slot /></thead>" },
  TableBody: { template: "<tbody><slot /></tbody>" },
  TableRow: { template: "<tr><slot /></tr>" },
  TableHead: { template: "<th><slot /></th>" },
  TableCell: { template: "<td><slot /></td>" },
  TableEmpty: { template: "<tr><td><slot /></td></tr>" },
  RouterLink: { template: "<a :href='to'><slot /></a>", props: ["to"] },
  IconGrowth: { template: "<span />" },
  IconMap2: { template: "<span />" },
  IconCircleFilled: { template: "<span />" },
  IconCircleCheck: { template: "<span />" },
}

const mountComponent = () =>
  mount(DashboardView, {
    global: {
      plugins: [createTestingPinia({ createSpy: vi.fn })],
      stubs,
    },
  })

beforeEach(() => {
  vi.clearAllMocks()
  setupMock()
})

describe("DashboardView", () => {
  describe("section headings", () => {
    it("renders the Plantings section heading", () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain("Plantings")
    })

    it("renders the Planting Locations section heading", () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain("Planting Locations")
    })
  })

  describe("plantings stat card", () => {
    it("shows the total plantings count", () => {
      const wrapper = mountComponent()

      const titles = wrapper.findAll('[data-test="card-title"]')
      expect(titles.some((t) => t.text() === "3")).toBe(true)
    })

    it("shows 0 when there are no plantings", () => {
      setupMock({ plantings: ref({ results: [], count: 0 }) })
      const wrapper = mountComponent()

      const titles = wrapper.findAll('[data-test="card-title"]')
      expect(titles.some((t) => t.text() === "0")).toBe(true)
    })
  })

  describe("location stat cards", () => {
    it("shows the total locations count", () => {
      const wrapper = mountComponent()

      const titles = wrapper.findAll('[data-test="card-title"]')
      // 3 locations total
      expect(titles.some((t) => t.text() === "3")).toBe(true)
    })

    it("shows the in-use count", () => {
      const wrapper = mountComponent()

      // 1 location is IN_USE
      const titles = wrapper.findAll('[data-test="card-title"]')
      expect(titles.some((t) => t.text() === "1")).toBe(true)
    })

    it("shows the available count including locations with no status", () => {
      const wrapper = mountComponent()

      // 1 AVAILABLE + 1 with null status = 2
      const titles = wrapper.findAll('[data-test="card-title"]')
      expect(titles.some((t) => t.text() === "2")).toBe(true)
    })

    it("shows 0 in-use when all locations are available", () => {
      setupMock(
        {},
        {
          locations: ref({
            results: [{ ...defaultLocations[1] }],
            count: 1,
          }),
        },
      )
      const wrapper = mountComponent()

      const titles = wrapper.findAll('[data-test="card-title"]')
      expect(titles.some((t) => t.text() === "0")).toBe(true)
    })
  })

  describe("recent plantings table", () => {
    it("renders planting rows with crop and variety names", () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain("Tomato")
      expect(wrapper.text()).toContain("Sun Gold")
      expect(wrapper.text()).toContain("Basil")
      expect(wrapper.text()).toContain("Genovese")
    })

    it("shows the most recent planting first", () => {
      const wrapper = mountComponent()

      const rows = wrapper.findAll("tbody tr")
      // Basil (Mar) is most recent, should appear before Tomato (Jan)
      expect(rows[0].text()).toContain("Basil")
    })

    it("shows at most 5 plantings", () => {
      const sixPlantings = Array.from({ length: 6 }, (_, i) => ({
        id: i + 1,
        crop: 1,
        cropName: `Crop ${i + 1}`,
        variety: 1,
        varietyName: `Variety ${i + 1}`,
        createdAt: new Date(2024, i, 1).toISOString(),
      }))

      setupMock({ plantings: ref({ results: sixPlantings, count: 6 }) })
      const wrapper = mountComponent()

      // First tbody is recent plantings, second is location overview
      const firstTbody = wrapper.findAll("tbody")[0]
      expect(firstTbody.findAll("tr")).toHaveLength(5)
    })

    it("shows empty state when there are no plantings", () => {
      setupMock({ plantings: ref({ results: [], count: 0 }) })
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain("No plantings yet.")
    })

    it("renders a View all link to /plantings", () => {
      const wrapper = mountComponent()

      const links = wrapper.findAll("a")
      expect(links.some((a) => a.attributes("href") === "/plantings")).toBe(true)
    })
  })

  describe("location overview table", () => {
    it("renders location rows with name and formatted type", () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain("Balcony Pot")
      expect(wrapper.text()).toContain("Pot")
      expect(wrapper.text()).toContain("Nursery A")
      expect(wrapper.text()).toContain("Nursery Pot")
      expect(wrapper.text()).toContain("Garden Bed")
      expect(wrapper.text()).toContain("Ground")
    })

    it("renders status badges for locations with a status", () => {
      const wrapper = mountComponent()

      const badges = wrapper.findAll('[data-test="badge"]')
      expect(badges.some((b) => b.text() === "In Use")).toBe(true)
      expect(badges.some((b) => b.text() === "Available")).toBe(true)
    })

    it("shows 'No status' for locations without a currentStatus", () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain("No status")
    })

    it("shows 'Damaged' label for damaged locations", () => {
      setupMock(
        {},
        {
          locations: ref({
            results: [
              {
                ...defaultLocations[0],
                currentStatus: {
                  id: 3,
                  status: "DAMAGED",
                  notes: "",
                  createdAt: "2024-03-01T00:00:00Z",
                },
              },
            ],
            count: 1,
          }),
        },
      )
      const wrapper = mountComponent()

      expect(wrapper.find('[data-test="badge"]').text()).toBe("Damaged")
    })

    it("shows empty state when there are no locations", () => {
      setupMock({}, { locations: ref({ results: [], count: 0 }) })
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain("No locations yet.")
    })

    it("renders a View all link to /planting-locations", () => {
      const wrapper = mountComponent()

      const links = wrapper.findAll("a")
      expect(links.some((a) => a.attributes("href") === "/planting-locations")).toBe(true)
    })
  })
})
