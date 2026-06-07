import { ref } from "vue"
import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import PlantingDailyObservationSheet from "@/components/plantings/daily-observation/PlantingDailyObservationSheet.vue"
import { createTestingPinia } from "@pinia/testing"

vi.mock("@/composables/usePlantingDailyObservations", () => ({
  usePlantingDailyObservations: vi.fn(),
}))

import { usePlantingDailyObservations } from "@/composables/usePlantingDailyObservations"

const mockCreateObservation = vi.fn()
const mockUpdateObservation = vi.fn()
const mockDeleteObservation = vi.fn()

const defaultObservations = {
  results: [
    {
      id: 1,
      stage: null,
      stageName: null,
      healthStatus: "GOOD",
      pestPressure: "NONE",
      diseaseSymptoms: false,
      watered: false,
      heightCm: "15.50",
      leafCount: 3,
      temperatureC: null,
      humidityPercent: null,
      lightHours: null,
      soilMoisturePercent: null,
      soilPh: null,
      ecMsCm: null,
      notes: "Healthy growth",
      image: null,
      createdAt: "2024-03-01T00:00:00Z",
      updatedAt: "2024-03-01T00:00:00Z",
    },
    {
      id: 2,
      stage: null,
      stageName: null,
      healthStatus: "POOR",
      pestPressure: "HIGH",
      diseaseSymptoms: true,
      watered: false,
      heightCm: null,
      leafCount: null,
      temperatureC: null,
      humidityPercent: null,
      lightHours: null,
      soilMoisturePercent: null,
      soilPh: null,
      ecMsCm: null,
      notes: "",
      image: null,
      createdAt: "2024-03-02T00:00:00Z",
      updatedAt: "2024-03-02T00:00:00Z",
    },
  ],
  count: 2,
}

function setupMock(overrides: Record<string, unknown> = {}) {
  vi.mocked(usePlantingDailyObservations).mockReturnValue({
    observations: ref(defaultObservations),
    isLoading: ref(false),
    isQueryError: ref(false),
    createError: ref(false),
    updateError: ref(false),
    deleteError: ref(false),
    isCreateSuccess: ref(false),
    isUpdateSuccess: ref(false),
    isDeleteSuccess: ref(false),
    createObservation: mockCreateObservation,
    updateObservation: mockUpdateObservation,
    deleteObservation: mockDeleteObservation,
    fetchObservations: vi.fn(),
    ...overrides,
  })
}

const stubs = {
  Sheet: { template: "<div><slot /></div>" },
  SheetContent: { template: "<div><slot /></div>" },
  SheetHeader: { template: "<div><slot /></div>" },
  SheetTitle: { template: "<div><slot /></div>" },
  SheetDescription: { template: "<div><slot /></div>" },
  Table: { template: "<table><slot /></table>" },
  TableHeader: { template: "<thead><slot /></thead>" },
  TableBody: { template: "<tbody><slot /></tbody>" },
  TableRow: { template: "<tr><slot /></tr>" },
  TableHead: { template: "<th><slot /></th>" },
  TableCell: { template: "<td><slot /></td>" },
  TableEmpty: { template: "<tr><td><slot /></td></tr>" },
  Badge: { template: "<span><slot /></span>" },
  Button: {
    template:
      "<button :disabled='disabled' @click=\"!disabled && $emit('click')\"><slot /></button>",
    props: ["disabled"],
    emits: ["click"],
  },
  AlertDialog: { template: "<div><slot /></div>", props: ["open"] },
  AlertDialogContent: { template: "<div><slot /></div>" },
  AlertDialogHeader: { template: "<div><slot /></div>" },
  AlertDialogTitle: { template: "<div><slot /></div>" },
  AlertDialogDescription: { template: "<div><slot /></div>" },
  AlertDialogFooter: { template: "<div><slot /></div>" },
  AlertDialogCancel: { template: "<button data-test='cancel'><slot /></button>" },
  AlertDialogAction: {
    template: "<button data-test='confirm' @click=\"$emit('click')\"><slot /></button>",
    emits: ["click"],
  },
  PlantingDailyObservationCreateDialog: {
    name: "PlantingDailyObservationCreateDialog",
    template: "<div data-test='create-dialog' :data-open='open' />",
    props: ["open", "isLoading", "isCreateSuccess"],
    emits: ["submit", "update:open"],
  },
  PlantingDailyObservationUpdateDialog: {
    name: "PlantingDailyObservationUpdateDialog",
    template: "<div data-test='update-dialog' :data-open='open' :data-id='id' />",
    props: ["open", "id", "observationFormInitialState", "isLoading", "isUpdateSuccess"],
    emits: ["submit", "update:open"],
  },
  PlantingDailyObservationViewDialog: {
    name: "PlantingDailyObservationViewDialog",
    template: "<div data-test='view-dialog' :data-open='open' />",
    props: ["open", "observation"],
    emits: ["update:open"],
  },
  IconLoader2: { template: "<span data-test='loader' />" },
  IconPlus: { template: "<span />" },
  IconPencil: { template: "<span />" },
  IconTrash: { template: "<span />" },
  IconEye: { template: "<span />" },
}

const mountComponent = (props = {}) =>
  mount(PlantingDailyObservationSheet, {
    props: { open: true, plantingId: 1, ...props },
    global: {
      plugins: [createTestingPinia({ createSpy: vi.fn })],
      stubs,
    },
  })

beforeEach(() => {
  vi.clearAllMocks()
  setupMock()
})

describe("PlantingDailyObservationSheet.vue", () => {
  describe("rendering", () => {
    it("renders observation rows with notes", () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain("Healthy growth")
    })

    it("renders — when heightCm is null", () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain("—")
    })

    it("shows empty state when there are no observations", () => {
      setupMock({ observations: ref({ results: [], count: 0 }) })
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain("No observations logged yet.")
    })

    it("shows loading spinner when isLoading is true and no observations exist", () => {
      setupMock({ observations: ref({ results: [], count: 0 }), isLoading: ref(true) })
      const wrapper = mountComponent()

      expect(wrapper.find('[data-test="loading-container"]').exists()).toBe(true)
    })

    it("does not show loading spinner when observations are already loaded", () => {
      setupMock({ isLoading: ref(true) })
      const wrapper = mountComponent()

      expect(wrapper.find('[data-test="loading-container"]').exists()).toBe(false)
    })
  })

  describe("create dialog", () => {
    it("create dialog is closed by default", () => {
      const wrapper = mountComponent()

      expect(wrapper.find('[data-test="create-dialog"]').attributes("data-open")).toBe("false")
    })

    it("opens create dialog when Add Observation button is clicked", async () => {
      const wrapper = mountComponent()

      const addButton = wrapper.findAll("button").find((b) => b.text().includes("Add Observation"))
      await addButton!.trigger("click")

      expect(wrapper.find('[data-test="create-dialog"]').attributes("data-open")).toBe("true")
    })

    it("calls createObservation when create dialog emits submit", async () => {
      mockCreateObservation.mockResolvedValue(undefined)
      const wrapper = mountComponent()

      const payload = {
        healthStatus: "GOOD",
        pestPressure: "NONE",
        diseaseSymptoms: false,
        notes: "Test",
      }
      await wrapper
        .findComponent({ name: "PlantingDailyObservationCreateDialog" })
        .vm.$emit("submit", payload, vi.fn())
      await wrapper.vm.$nextTick()

      expect(mockCreateObservation).toHaveBeenCalledWith(payload)
    })

    it("calls the onError callback when createObservation fails", async () => {
      const error = new Error("API error")
      mockCreateObservation.mockRejectedValue(error)
      const wrapper = mountComponent()

      const onError = vi.fn()
      await wrapper
        .findComponent({ name: "PlantingDailyObservationCreateDialog" })
        .vm.$emit(
          "submit",
          { healthStatus: "GOOD", pestPressure: "NONE", diseaseSymptoms: false },
          onError,
        )
      await wrapper.vm.$nextTick()

      expect(onError).toHaveBeenCalledWith(error)
    })
  })

  describe("view dialog", () => {
    it("opens view dialog when eye button is clicked", async () => {
      const wrapper = mountComponent()

      const iconButtons = wrapper.findAll("button").filter((b) => !b.text())
      await iconButtons[0].trigger("click")

      expect(wrapper.find('[data-test="view-dialog"]').attributes("data-open")).toBe("true")
    })
  })

  describe("update dialog", () => {
    it("update dialog is not rendered until edit is clicked", () => {
      const wrapper = mountComponent()

      expect(wrapper.find('[data-test="update-dialog"]').exists()).toBe(false)
    })

    it("opens update dialog with correct id when edit button is clicked", async () => {
      const wrapper = mountComponent()

      // icon buttons per row: [eye, pencil, trash] × 2 rows — pencil for row 1 is index 1
      const iconButtons = wrapper.findAll("button").filter((b) => !b.text())
      await iconButtons[1].trigger("click")

      const updateDialog = wrapper.find('[data-test="update-dialog"]')
      expect(updateDialog.attributes("data-open")).toBe("true")
      expect(updateDialog.attributes("data-id")).toBe("1")
    })

    it("opens update dialog with correct id for the second row", async () => {
      const wrapper = mountComponent()

      // icon buttons: [eye1, pencil1, trash1, eye2, pencil2, trash2] — pencil2 is index 4
      const iconButtons = wrapper.findAll("button").filter((b) => !b.text())
      await iconButtons[4].trigger("click")

      const updateDialog = wrapper.find('[data-test="update-dialog"]')
      expect(updateDialog.attributes("data-id")).toBe("2")
    })

    it("calls updateObservation when update dialog emits submit", async () => {
      mockUpdateObservation.mockResolvedValue(undefined)
      const wrapper = mountComponent()

      const iconButtons = wrapper.findAll("button").filter((b) => !b.text())
      await iconButtons[1].trigger("click")
      await wrapper.vm.$nextTick()

      const payload = {
        healthStatus: "FAIR",
        pestPressure: "NONE",
        diseaseSymptoms: false,
        notes: "",
      }
      await wrapper
        .findComponent({ name: "PlantingDailyObservationUpdateDialog" })
        .vm.$emit("submit", 1, payload, vi.fn())
      await wrapper.vm.$nextTick()

      expect(mockUpdateObservation).toHaveBeenCalledWith({ id: 1, payload })
    })

    it("calls the onError callback when updateObservation fails", async () => {
      const error = new Error("API error")
      mockUpdateObservation.mockRejectedValue(error)
      const wrapper = mountComponent()

      const iconButtons = wrapper.findAll("button").filter((b) => !b.text())
      await iconButtons[1].trigger("click")
      await wrapper.vm.$nextTick()

      const onError = vi.fn()
      await wrapper
        .findComponent({ name: "PlantingDailyObservationUpdateDialog" })
        .vm.$emit(
          "submit",
          1,
          { healthStatus: "FAIR", pestPressure: "NONE", diseaseSymptoms: false },
          onError,
        )
      await wrapper.vm.$nextTick()

      expect(onError).toHaveBeenCalledWith(error)
    })
  })

  describe("delete", () => {
    it("opens delete confirmation dialog when trash button is clicked", async () => {
      const wrapper = mountComponent()

      // trash for row 1 is index 2
      const iconButtons = wrapper.findAll("button").filter((b) => !b.text())
      await iconButtons[2].trigger("click")

      expect(wrapper.find('[data-test="confirm"]').exists()).toBe(true)
    })

    it("calls deleteObservation with correct id when confirm is clicked", async () => {
      mockDeleteObservation.mockResolvedValue(undefined)
      const wrapper = mountComponent()

      const iconButtons = wrapper.findAll("button").filter((b) => !b.text())
      await iconButtons[2].trigger("click")
      await wrapper.find('[data-test="confirm"]').trigger("click")
      await wrapper.vm.$nextTick()

      expect(mockDeleteObservation).toHaveBeenCalledWith(1)
    })

    it("calls deleteObservation with the second row id when that trash button is clicked", async () => {
      mockDeleteObservation.mockResolvedValue(undefined)
      const wrapper = mountComponent()

      // trash for row 2 is index 5
      const iconButtons = wrapper.findAll("button").filter((b) => !b.text())
      await iconButtons[5].trigger("click")
      await wrapper.find('[data-test="confirm"]').trigger("click")
      await wrapper.vm.$nextTick()

      expect(mockDeleteObservation).toHaveBeenCalledWith(2)
    })
  })

  describe("pagination", () => {
    const manyObservations = { results: defaultObservations.results, count: 25 }

    it("does not show pagination when there are no observations", () => {
      setupMock({ observations: ref({ results: [], count: 0 }) })
      const wrapper = mountComponent()

      expect(wrapper.findAll("button").find((b) => b.text().includes("Previous"))).toBeUndefined()
      expect(wrapper.findAll("button").find((b) => b.text().includes("Next"))).toBeUndefined()
    })

    it("shows correct page counter", () => {
      setupMock({ observations: ref(manyObservations) })
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain("Page 1 of 3")
    })

    it("disables Previous button on first page", () => {
      setupMock({ observations: ref(manyObservations) })
      const wrapper = mountComponent()

      const prevButton = wrapper.findAll("button").find((b) => b.text().includes("Previous"))
      expect(prevButton!.attributes("disabled")).toBeDefined()
    })

    it("enables Next button when not on last page", () => {
      setupMock({ observations: ref(manyObservations) })
      const wrapper = mountComponent()

      const nextButton = wrapper.findAll("button").find((b) => b.text().includes("Next"))
      expect(nextButton!.attributes("disabled")).toBeUndefined()
    })

    it("disables Next button on last page", () => {
      setupMock({ observations: ref({ results: defaultObservations.results, count: 2 }) })
      const wrapper = mountComponent()

      const nextButton = wrapper.findAll("button").find((b) => b.text().includes("Next"))
      expect(nextButton!.attributes("disabled")).toBeDefined()
    })

    it("advances to next page when Next is clicked", async () => {
      setupMock({ observations: ref(manyObservations) })
      const wrapper = mountComponent()

      await wrapper
        .findAll("button")
        .find((b) => b.text().includes("Next"))!
        .trigger("click")

      expect(wrapper.text()).toContain("Page 2 of 3")
    })

    it("goes back to previous page when Previous is clicked", async () => {
      setupMock({ observations: ref(manyObservations) })
      const wrapper = mountComponent()

      await wrapper
        .findAll("button")
        .find((b) => b.text().includes("Next"))!
        .trigger("click")
      await wrapper
        .findAll("button")
        .find((b) => b.text().includes("Previous"))!
        .trigger("click")

      expect(wrapper.text()).toContain("Page 1 of 3")
    })

    it("resets to first page after delete", async () => {
      mockDeleteObservation.mockResolvedValue(undefined)
      setupMock({ observations: ref(manyObservations) })
      const wrapper = mountComponent()

      await wrapper
        .findAll("button")
        .find((b) => b.text().includes("Next"))!
        .trigger("click")
      expect(wrapper.text()).toContain("Page 2 of 3")

      // trash for row 1 is index 2
      const iconButtons = wrapper.findAll("button").filter((b) => !b.text())
      await iconButtons[2].trigger("click")
      await wrapper.find('[data-test="confirm"]').trigger("click")
      await wrapper.vm.$nextTick()

      expect(wrapper.text()).toContain("Page 1 of 3")
    })

    it("resets to first page after create", async () => {
      mockCreateObservation.mockResolvedValue(undefined)
      setupMock({ observations: ref(manyObservations) })
      const wrapper = mountComponent()

      await wrapper
        .findAll("button")
        .find((b) => b.text().includes("Next"))!
        .trigger("click")
      expect(wrapper.text()).toContain("Page 2 of 3")

      const payload = {
        healthStatus: "GOOD",
        pestPressure: "NONE",
        diseaseSymptoms: false,
        notes: "",
      }
      await wrapper
        .findComponent({ name: "PlantingDailyObservationCreateDialog" })
        .vm.$emit("submit", payload, vi.fn())
      await wrapper.vm.$nextTick()

      expect(wrapper.text()).toContain("Page 1 of 3")
    })
  })
})
