import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import { ref } from "vue"
import PlantingLocationStatusHistoryDialog from "@/components/planting-locations/PlantingLocationStatusHistoryDialog.vue"
import type { PlantingLocationStatus } from "@/types/plantingLocationStatus"

const mockStatuses = ref<{ results: PlantingLocationStatus[]; count: number } | null>(null)
const mockIsLoading = ref(false)

vi.mock("@/composables/usePlantingLocationStatuses", () => ({
  usePlantingLocationStatuses: vi.fn(() => ({
    statuses: mockStatuses,
    isLoading: mockIsLoading,
    isQueryError: ref(false),
    createError: ref(false),
    isCreateSuccess: ref(false),
    createStatus: vi.fn(),
  })),
}))

const stubs = {
  Dialog: { template: "<div><slot /></div>" },
  DialogContent: { template: "<div><slot /></div>" },
  DialogHeader: { template: "<div><slot /></div>" },
  DialogTitle: { template: "<div><slot /></div>" },
  DialogDescription: { template: "<div><slot /></div>" },
  Badge: { template: "<span><slot /></span>" },
}

const mountComponent = (props = {}) =>
  mount(PlantingLocationStatusHistoryDialog, {
    props: {
      open: true,
      locationId: 1,
      ...props,
    },
    global: { stubs },
  })

const makeEntry = (overrides: Partial<PlantingLocationStatus> = {}): PlantingLocationStatus => ({
  id: 1,
  status: "DAMAGED",
  notes: "Cracked from heat.",
  image: null,
  createdAt: "2024-03-01T00:00:00Z",
  ...overrides,
})

beforeEach(() => {
  vi.clearAllMocks()
  mockStatuses.value = null
  mockIsLoading.value = false
})

describe("PlantingLocationStatusHistoryDialog.vue", () => {
  describe("loading state", () => {
    it("renders loading spinner when isLoading is true", () => {
      mockIsLoading.value = true
      const wrapper = mountComponent()

      expect(wrapper.find(".animate-spin").exists()).toBe(true)
    })
  })

  describe("empty state", () => {
    it("renders empty message when statuses results is empty", () => {
      mockStatuses.value = { results: [], count: 0 }
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain("No status entries recorded yet.")
    })

    it("renders empty message when statuses is null", () => {
      mockStatuses.value = null
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain("No status entries recorded yet.")
    })
  })

  describe("populated state", () => {
    it("renders one list item per entry", () => {
      mockStatuses.value = {
        results: [makeEntry({ id: 1 }), makeEntry({ id: 2, status: "RETIRED" })],
        count: 2,
      }
      const wrapper = mountComponent()

      expect(wrapper.findAll("li")).toHaveLength(2)
    })

    it("displays the status label text for each entry", () => {
      mockStatuses.value = {
        results: [makeEntry({ status: "DAMAGED" })],
        count: 1,
      }
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain("Damaged")
    })

    it("displays notes when present", () => {
      mockStatuses.value = {
        results: [makeEntry({ notes: "Cracked from heat." })],
        count: 1,
      }
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain("Cracked from heat.")
    })

    it("renders img element when entry has an image", () => {
      mockStatuses.value = {
        results: [makeEntry({ image: "http://example.com/photo.jpg" })],
        count: 1,
      }
      const wrapper = mountComponent()

      expect(wrapper.find("img").exists()).toBe(true)
      expect(wrapper.find("img").attributes("src")).toBe("http://example.com/photo.jpg")
    })

    it("omits img element when entry has no image", () => {
      mockStatuses.value = {
        results: [makeEntry({ image: null })],
        count: 1,
      }
      const wrapper = mountComponent()

      expect(wrapper.find("img").exists()).toBe(false)
    })

    it("displays a formatted date string", () => {
      mockStatuses.value = {
        results: [makeEntry({ createdAt: "2024-03-01T00:00:00Z" })],
        count: 1,
      }
      const wrapper = mountComponent()

      // The date should be formatted and present (exact string depends on locale)
      expect(wrapper.find(".text-xs").exists()).toBe(true)
      expect(wrapper.find(".text-xs").text()).not.toBe("")
    })
  })
})
