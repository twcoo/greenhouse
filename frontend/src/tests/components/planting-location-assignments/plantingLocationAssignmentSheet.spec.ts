import { ref } from "vue"
import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import PlantingLocationAssignmentSheet from "@/components/planting-location-assignments/PlantingLocationAssignmentSheet.vue"
import { createTestingPinia } from "@pinia/testing"

vi.mock("@/composables/usePlantingLocationAssignments", () => ({
  usePlantingLocationAssignments: vi.fn(),
}))

import { usePlantingLocationAssignments } from "@/composables/usePlantingLocationAssignments"

const mockCreateAssignment = vi.fn()
const mockUpdateAssignment = vi.fn()
const mockDeleteAssignment = vi.fn()

const defaultAssignments = {
  results: [
    {
      id: 1,
      plantingLocation: 2,
      plantingLocationName: "Balcony Pot",
      startDate: "2024-03-01",
      endDate: "2024-09-01",
      createdAt: "2024-03-01T00:00:00Z",
      updatedAt: "2024-03-01T00:00:00Z",
    },
    {
      id: 2,
      plantingLocation: 3,
      plantingLocationName: "Garden Bed",
      startDate: "2024-01-01",
      endDate: null,
      createdAt: "2024-01-01T00:00:00Z",
      updatedAt: "2024-01-01T00:00:00Z",
    },
  ],
  count: 2,
}

function setupMock(overrides: Record<string, unknown> = {}) {
  vi.mocked(usePlantingLocationAssignments).mockReturnValue({
    assignments: ref(defaultAssignments),
    isLoading: ref(false),
    isCreateSuccess: ref(false),
    isUpdateSuccess: ref(false),
    isQueryError: ref(false),
    createError: ref(false),
    updateError: ref(false),
    deleteError: ref(false),
    isDeleteSuccess: ref(false),
    createAssignment: mockCreateAssignment,
    updateAssignment: mockUpdateAssignment,
    deleteAssignment: mockDeleteAssignment,
    fetchAssignments: vi.fn(),
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
  Button: {
    template: "<button @click=\"$emit('click')\"><slot /></button>",
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
  PlantingLocationAssignmentCreateDialog: {
    name: "PlantingLocationAssignmentCreateDialog",
    template: "<div data-test='create-dialog' :data-open='open' />",
    props: ["open", "isLoading", "isCreateSuccess"],
    emits: ["submit", "update:open"],
  },
  PlantingLocationAssignmentUpdateDialog: {
    name: "PlantingLocationAssignmentUpdateDialog",
    template: "<div data-test='update-dialog' :data-open='open' :data-id='id' />",
    props: ["open", "id", "assignmentFormInitialState", "isLoading", "isUpdateSuccess"],
    emits: ["submit", "update:open"],
  },
  IconLoader2: { template: "<span data-test='loader' />" },
  IconPlus: { template: "<span />" },
  IconPencil: { template: "<span />" },
  IconTrash: { template: "<span />" },
}

const mountComponent = (props = {}) =>
  mount(PlantingLocationAssignmentSheet, {
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

describe("PlantingLocationAssignmentSheet.vue", () => {
  it("renders assignment rows with location name, start, and end dates", () => {
    const wrapper = mountComponent()

    expect(wrapper.text()).toContain("Balcony Pot")
    expect(wrapper.text()).toContain("Garden Bed")
  })

  it("shows 'Present' for assignments with no end date", () => {
    const wrapper = mountComponent()

    expect(wrapper.text()).toContain("Present")
  })

  it("shows 'No location assignments yet.' when there are no assignments", () => {
    setupMock({ assignments: ref({ results: [], count: 0 }) })
    const wrapper = mountComponent()

    expect(wrapper.text()).toContain("No location assignments yet.")
  })

  it("shows loading spinner when isLoading is true and there are no assignments", () => {
    setupMock({ assignments: ref({ results: [], count: 0 }), isLoading: ref(true) })
    const wrapper = mountComponent()

    expect(wrapper.find('[data-test="loading-container"]').exists()).toBe(true)
  })

  it("does not show loading spinner when assignments are already loaded", () => {
    setupMock({ isLoading: ref(true) })
    const wrapper = mountComponent()

    expect(wrapper.find('[data-test="loading-container"]').exists()).toBe(false)
  })

  it("opens create dialog when Add Assignment button is clicked", async () => {
    const wrapper = mountComponent()

    const createDialog = wrapper.find('[data-test="create-dialog"]')
    expect(createDialog.attributes("data-open")).toBe("false")

    await wrapper.findAll("button")[0].trigger("click")

    expect(wrapper.find('[data-test="create-dialog"]').attributes("data-open")).toBe("true")
  })

  it("opens update dialog with correct id when edit is clicked", async () => {
    const wrapper = mountComponent()

    // icon buttons: [edit1, delete1, edit2, delete2] — edit1 is index 0
    const iconButtons = wrapper.findAll("button").filter((b) => !b.text())
    await iconButtons[0].trigger("click")

    const updateDialog = wrapper.find('[data-test="update-dialog"]')
    expect(updateDialog.attributes("data-open")).toBe("true")
    expect(updateDialog.attributes("data-id")).toBe("1")
  })

  it("opens delete confirmation dialog when delete button is clicked", async () => {
    const wrapper = mountComponent()

    // icon buttons: [edit1, delete1, edit2, delete2] — delete1 is index 1
    const iconButtons = wrapper.findAll("button").filter((b) => !b.text())
    await iconButtons[1].trigger("click")

    expect(wrapper.find('[data-test="confirm"]').exists()).toBe(true)
  })

  it("calls deleteAssignment with the correct id when confirm is clicked", async () => {
    mockDeleteAssignment.mockResolvedValue(undefined)
    const wrapper = mountComponent()

    // click delete on first row (id=1)
    const iconButtons = wrapper.findAll("button").filter((b) => !b.text())
    await iconButtons[1].trigger("click")
    await wrapper.find('[data-test="confirm"]').trigger("click")
    await wrapper.vm.$nextTick()

    expect(mockDeleteAssignment).toHaveBeenCalledWith(1)
  })

  it("calls createAssignment when the create dialog emits submit", async () => {
    mockCreateAssignment.mockResolvedValue(undefined)
    const wrapper = mountComponent()

    const payload = { plantingLocation: 2, startDate: "2024-03-01" }
    await wrapper
      .findComponent({ name: "PlantingLocationAssignmentCreateDialog" })
      .vm.$emit("submit", payload, vi.fn())
    await wrapper.vm.$nextTick()

    expect(mockCreateAssignment).toHaveBeenCalledWith(payload)
  })

  it("calls the onError callback when createAssignment fails", async () => {
    const error = new Error("API error")
    mockCreateAssignment.mockRejectedValue(error)
    const wrapper = mountComponent()

    const onError = vi.fn()
    await wrapper
      .findComponent({ name: "PlantingLocationAssignmentCreateDialog" })
      .vm.$emit("submit", { plantingLocation: 2, startDate: "2024-03-01" }, onError)
    await wrapper.vm.$nextTick()

    expect(onError).toHaveBeenCalledWith(error)
  })

  it("calls updateAssignment when the update dialog emits submit", async () => {
    mockUpdateAssignment.mockResolvedValue(undefined)
    const wrapper = mountComponent()

    // open update dialog first
    const iconButtons = wrapper.findAll("button").filter((b) => !b.text())
    await iconButtons[0].trigger("click")
    await wrapper.vm.$nextTick()

    const payload = { plantingLocation: 2, startDate: "2024-03-01", endDate: "2024-09-01" }
    await wrapper
      .findComponent({ name: "PlantingLocationAssignmentUpdateDialog" })
      .vm.$emit("submit", 1, payload, vi.fn())
    await wrapper.vm.$nextTick()

    expect(mockUpdateAssignment).toHaveBeenCalledWith({ id: 1, payload })
  })

  it("calls the onError callback when updateAssignment fails", async () => {
    const error = new Error("API error")
    mockUpdateAssignment.mockRejectedValue(error)
    const wrapper = mountComponent()

    const iconButtons = wrapper.findAll("button").filter((b) => !b.text())
    await iconButtons[0].trigger("click")
    await wrapper.vm.$nextTick()

    const onError = vi.fn()
    const payload = { plantingLocation: 2, startDate: "2024-03-01" }
    await wrapper
      .findComponent({ name: "PlantingLocationAssignmentUpdateDialog" })
      .vm.$emit("submit", 1, payload, onError)
    await wrapper.vm.$nextTick()

    expect(onError).toHaveBeenCalledWith(error)
  })
})
