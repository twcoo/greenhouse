import { ref } from "vue"
import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import PlantingLocationStatusSheet from "@/components/planting-locations/status/PlantingLocationStatusSheet.vue"
import type { PlantingLocationStatus } from "@/types/plantingLocationStatus"

vi.mock("@/composables/usePlantingLocationStatuses", () => ({
  usePlantingLocationStatuses: vi.fn(),
}))

import { usePlantingLocationStatuses } from "@/composables/usePlantingLocationStatuses"

const mockCreateStatus = vi.fn()

const makeEntry = (overrides: Partial<PlantingLocationStatus> = {}): PlantingLocationStatus => ({
  id: 1,
  status: "DAMAGED",
  notes: "Cracked from heat.",
  image: null,
  createdAt: "2024-03-01T00:00:00Z",
  ...overrides,
})

const defaultStatuses = {
  results: [makeEntry({ id: 1 }), makeEntry({ id: 2, status: "RETIRED", notes: "Old pot." })],
  count: 2,
}

function setupMock(overrides: Record<string, unknown> = {}) {
  vi.mocked(usePlantingLocationStatuses).mockReturnValue({
    statuses: ref(defaultStatuses),
    isLoading: ref(false),
    isCreateSuccess: ref(false),
    isQueryError: ref(false),
    createError: ref(false),
    createStatus: mockCreateStatus,
    ...overrides,
  })
}

const inUseStatus: PlantingLocationStatus = {
  id: 99,
  status: "IN_USE",
  notes: "",
  image: null,
  createdAt: "2024-03-01T00:00:00Z",
}

const stubs = {
  Sheet: { template: "<div><slot /></div>" },
  SheetContent: { template: "<div><slot /></div>" },
  SheetHeader: { template: "<div><slot /></div>" },
  SheetTitle: { template: "<div><slot /></div>" },
  SheetDescription: { template: "<div><slot /></div>" },
  Badge: { template: "<span><slot /></span>" },
  Button: {
    template:
      "<button :disabled='disabled' @click=\"!disabled && $emit('click')\"><slot /></button>",
    props: ["disabled"],
    emits: ["click"],
  },
  Dialog: { template: "<div><slot /></div>", props: ["open"] },
  DialogContent: { template: "<div><slot /></div>" },
  PlantingLocationSetStatusDialog: {
    name: "PlantingLocationSetStatusDialog",
    template: "<div data-test='set-status-dialog' />",
    props: ["open", "currentStatus", "isLoading", "isCreateSuccess"],
    emits: ["update:open", "submit"],
  },
  IconLoader2: { template: "<span data-test='loader' />" },
  IconPlus: { template: "<span />" },
}

const mountComponent = (props = {}) =>
  mount(PlantingLocationStatusSheet, {
    props: { open: true, locationId: 1, currentStatus: null, ...props },
    global: { stubs },
  })

beforeEach(() => {
  vi.clearAllMocks()
  setupMock()
})

describe("PlantingLocationStatusSheet.vue", () => {
  describe("loading state", () => {
    it("shows loading spinner when isLoading is true and no entries exist", () => {
      setupMock({ statuses: ref({ results: [], count: 0 }), isLoading: ref(true) })
      const wrapper = mountComponent()

      expect(wrapper.find('[data-test="loading-container"]').exists()).toBe(true)
    })

    it("does not show loading spinner when entries are already loaded", () => {
      setupMock({ isLoading: ref(true) })
      const wrapper = mountComponent()

      expect(wrapper.find('[data-test="loading-container"]').exists()).toBe(false)
    })
  })

  describe("empty state", () => {
    it("shows empty message when there are no status entries", () => {
      setupMock({ statuses: ref({ results: [], count: 0 }) })
      const wrapper = mountComponent()

      expect(wrapper.find('[data-test="empty-state"]').exists()).toBe(true)
      expect(wrapper.text()).toContain("No status entries recorded yet.")
    })

    it("hides status list when there are no entries", () => {
      setupMock({ statuses: ref({ results: [], count: 0 }) })
      const wrapper = mountComponent()

      expect(wrapper.find('[data-test="status-list"]').exists()).toBe(false)
    })
  })

  describe("populated state", () => {
    it("renders one list item per entry", () => {
      const wrapper = mountComponent()

      expect(wrapper.findAll("li")).toHaveLength(2)
    })

    it("displays status label for each entry", () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain("Damaged")
      expect(wrapper.text()).toContain("Retired")
    })

    it("displays notes for each entry", () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain("Cracked from heat.")
      expect(wrapper.text()).toContain("Old pot.")
    })

    it("renders image thumbnail when entry has an image", () => {
      setupMock({
        statuses: ref({
          results: [makeEntry({ image: "http://example.com/photo.jpg" })],
          count: 1,
        }),
      })
      const wrapper = mountComponent()

      expect(wrapper.find('[data-test="image-thumbnail"]').exists()).toBe(true)
      expect(wrapper.find('[data-test="image-thumbnail"] img').attributes("src")).toBe(
        "http://example.com/photo.jpg",
      )
    })

    it("omits image thumbnail when entry has no image", () => {
      setupMock({ statuses: ref({ results: [makeEntry({ image: null })], count: 1 }) })
      const wrapper = mountComponent()

      expect(wrapper.find('[data-test="image-thumbnail"]').exists()).toBe(false)
    })
  })

  describe("Set Status button", () => {
    it("is enabled when currentStatus is null", () => {
      const wrapper = mountComponent({ currentStatus: null })

      const btn = wrapper.find('[data-test="set-status-button"]')
      expect(btn.attributes("disabled")).toBeUndefined()
    })

    it("is enabled when currentStatus is not IN_USE", () => {
      const wrapper = mountComponent({ currentStatus: makeEntry({ status: "DAMAGED" }) })

      const btn = wrapper.find('[data-test="set-status-button"]')
      expect(btn.attributes("disabled")).toBeUndefined()
    })

    it("is disabled when currentStatus is IN_USE", () => {
      const wrapper = mountComponent({ currentStatus: inUseStatus })

      const btn = wrapper.find('[data-test="set-status-button"]')
      expect(btn.attributes("disabled")).toBeDefined()
    })

    it("opens the set status dialog when clicked", async () => {
      const wrapper = mountComponent()

      expect(wrapper.find('[data-test="set-status-dialog"]').exists()).toBe(false)

      await wrapper.find('[data-test="set-status-button"]').trigger("click")

      expect(wrapper.find('[data-test="set-status-dialog"]').exists()).toBe(true)
    })

    it("calls createStatus when dialog emits submit", async () => {
      mockCreateStatus.mockResolvedValue(undefined)
      const wrapper = mountComponent()

      await wrapper.find('[data-test="set-status-button"]').trigger("click")
      await wrapper.vm.$nextTick()

      const payload = { status: "DAMAGED" as const, notes: "Cracked." }
      await wrapper
        .findComponent({ name: "PlantingLocationSetStatusDialog" })
        .vm.$emit("submit", payload, vi.fn())
      await wrapper.vm.$nextTick()

      expect(mockCreateStatus).toHaveBeenCalledWith({ id: 1, payload })
    })

    it("calls onError callback when createStatus fails", async () => {
      const error = new Error("API error")
      mockCreateStatus.mockRejectedValue(error)
      const wrapper = mountComponent()

      await wrapper.find('[data-test="set-status-button"]').trigger("click")
      await wrapper.vm.$nextTick()

      const onError = vi.fn()
      await wrapper
        .findComponent({ name: "PlantingLocationSetStatusDialog" })
        .vm.$emit("submit", { status: "DAMAGED" as const }, onError)
      await wrapper.vm.$nextTick()

      expect(onError).toHaveBeenCalledWith(error)
    })
  })

  describe("pagination", () => {
    const manyStatuses = { results: defaultStatuses.results, count: 25 }

    it("does not show pagination when there are no entries", () => {
      setupMock({ statuses: ref({ results: [], count: 0 }) })
      const wrapper = mountComponent()

      expect(wrapper.find('[data-test="pagination"]').exists()).toBe(false)
    })

    it("shows correct page counter", () => {
      setupMock({ statuses: ref(manyStatuses) })
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain("Page 1 of 3")
    })

    it("disables Previous button on first page", () => {
      setupMock({ statuses: ref(manyStatuses) })
      const wrapper = mountComponent()

      const prevButton = wrapper.find('[data-test="prev-button"]')
      expect(prevButton.attributes("disabled")).toBeDefined()
    })

    it("enables Next button when not on last page", () => {
      setupMock({ statuses: ref(manyStatuses) })
      const wrapper = mountComponent()

      const nextButton = wrapper.find('[data-test="next-button"]')
      expect(nextButton.attributes("disabled")).toBeUndefined()
    })

    it("disables Next button on last page", () => {
      setupMock({ statuses: ref({ results: defaultStatuses.results, count: 2 }) })
      const wrapper = mountComponent()

      const nextButton = wrapper.find('[data-test="next-button"]')
      expect(nextButton.attributes("disabled")).toBeDefined()
    })

    it("advances to next page when Next is clicked", async () => {
      setupMock({ statuses: ref(manyStatuses) })
      const wrapper = mountComponent()

      await wrapper.find('[data-test="next-button"]').trigger("click")

      expect(wrapper.text()).toContain("Page 2 of 3")
    })

    it("goes back to previous page when Previous is clicked", async () => {
      setupMock({ statuses: ref(manyStatuses) })
      const wrapper = mountComponent()

      await wrapper.find('[data-test="next-button"]').trigger("click")
      await wrapper.find('[data-test="prev-button"]').trigger("click")

      expect(wrapper.text()).toContain("Page 1 of 3")
    })

    it("resets to first page after create success", async () => {
      const isCreateSuccess = ref(false)
      setupMock({ statuses: ref(manyStatuses), isCreateSuccess })
      const wrapper = mountComponent()

      await wrapper.find('[data-test="next-button"]').trigger("click")
      expect(wrapper.text()).toContain("Page 2 of 3")

      isCreateSuccess.value = true
      await wrapper.vm.$nextTick()

      expect(wrapper.text()).toContain("Page 1 of 3")
    })
  })
})
