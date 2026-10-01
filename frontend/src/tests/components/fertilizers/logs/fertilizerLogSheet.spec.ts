import { ref } from "vue"
import { flushPromises, mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import FertilizerLogSheet from "@/components/fertilizers/logs/FertilizerLogSheet.vue"
import { createTestingPinia } from "@pinia/testing"
import type { Fertilizer } from "@/types/fertilizer"

vi.mock("@/composables/useFertilizerLogs", () => ({
  useFertilizerLogs: vi.fn(),
}))

import { useFertilizerLogs } from "@/composables/useFertilizerLogs"

const mockCreateLog = vi.fn()
const mockUpdateLog = vi.fn()
const mockDeleteLog = vi.fn()

const defaultLogs = {
  results: [
    {
      id: 1,
      eventType: "ADDED_INGREDIENT",
      itemAdded: "banana peels",
      quantity: "2 kg",
      notes: "Chopped first.",
      logDate: "2024-03-01",
      createdAt: "2024-03-01T00:00:00Z",
      updatedAt: "2024-03-01T00:00:00Z",
    },
    {
      id: 2,
      eventType: "ADDED_WATER",
      itemAdded: "",
      quantity: "5 liters",
      notes: "",
      logDate: "2024-03-02",
      createdAt: "2024-03-02T00:00:00Z",
      updatedAt: "2024-03-02T00:00:00Z",
    },
  ],
  count: 2,
}

function setupMock(overrides: Record<string, unknown> = {}) {
  vi.mocked(useFertilizerLogs).mockReturnValue({
    logs: ref(defaultLogs),
    isLoading: ref(false),
    isQueryError: ref(false),
    createError: ref(false),
    updateError: ref(false),
    deleteError: ref(false),
    isCreateSuccess: ref(false),
    isUpdateSuccess: ref(false),
    isDeleteSuccess: ref(false),
    createLog: mockCreateLog,
    updateLog: mockUpdateLog,
    deleteLog: mockDeleteLog,
    fetchLogs: vi.fn(),
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
  FertilizerLogCreateDialog: {
    name: "FertilizerLogCreateDialog",
    template: "<div data-test='create-dialog' :data-open='open' />",
    props: ["open", "isLoading", "isCreateSuccess", "fertilizerName"],
    emits: ["submit", "update:open"],
  },
  FertilizerLogUpdateDialog: {
    name: "FertilizerLogUpdateDialog",
    template: "<div data-test='update-dialog' :data-open='open' :data-id='id' />",
    props: ["open", "id", "logFormInitialState", "isLoading", "isUpdateSuccess"],
    emits: ["submit", "update:open"],
  },
  FertilizerLogViewDialog: {
    name: "FertilizerLogViewDialog",
    template: "<div data-test='view-dialog' :data-open='open' />",
    props: ["open", "log"],
    emits: ["update:open"],
  },
  IconLoader2: { template: "<span data-test='loader' />" },
  IconPlus: { template: "<span />" },
  IconPencil: { template: "<span />" },
  IconTrash: { template: "<span />" },
  IconEye: { template: "<span />" },
}

const mockFertilizer: Fertilizer = {
  id: 1,
  name: "Swamp Fertilizer #1",
  type: "SWAMP",
  status: "BREWING",
  startDate: "2024-01-01",
  ingredients: ["banana peels"],
  notes: "",
  createdAt: "2024-01-01T00:00:00Z",
  updatedAt: "2024-01-01T00:00:00Z",
}

const mountComponent = (props = {}) =>
  mount(FertilizerLogSheet, {
    props: { open: true, fertilizerId: 1, fertilizer: mockFertilizer, ...props },
    global: {
      plugins: [createTestingPinia({ createSpy: vi.fn })],
      stubs,
    },
  })

beforeEach(() => {
  vi.clearAllMocks()
  setupMock()
})

describe("FertilizerLogSheet.vue", () => {
  it("renders log rows with item names", () => {
    const wrapper = mountComponent()

    expect(wrapper.text()).toContain("banana peels")
  })

  it("shows empty state when there are no logs", () => {
    setupMock({ logs: ref({ results: [], count: 0 }) })
    const wrapper = mountComponent()

    expect(wrapper.text()).toContain("No logs recorded yet.")
  })

  it("shows loading spinner when isLoading and no logs exist", () => {
    setupMock({ logs: ref({ results: [], count: 0 }), isLoading: ref(true) })
    const wrapper = mountComponent()

    expect(wrapper.find('[data-test="loading-container"]').exists()).toBe(true)
  })

  it("calls createLog when create dialog emits submit", async () => {
    mockCreateLog.mockResolvedValue(undefined)
    const wrapper = mountComponent()

    const payload = {
      logDate: "2024-03-01",
      eventType: "ADDED_WATER",
      itemAdded: "",
      quantity: "5 liters",
      notes: "",
    }
    await wrapper
      .findComponent({ name: "FertilizerLogCreateDialog" })
      .vm.$emit("submit", payload, vi.fn())
    await wrapper.vm.$nextTick()

    expect(mockCreateLog).toHaveBeenCalledWith(payload)
  })

  it("calls deleteLog with correct id when confirm is clicked", async () => {
    mockDeleteLog.mockResolvedValue(undefined)
    const wrapper = mountComponent()

    const iconButtons = wrapper.findAll("button").filter((b) => !b.text())
    await iconButtons[2].trigger("click")
    await wrapper.find('[data-test="confirm"]').trigger("click")
    await wrapper.vm.$nextTick()

    expect(mockDeleteLog).toHaveBeenCalledWith(1)
  })

  it("passes the fertilizer id ref to the composable", () => {
    mountComponent()

    const idRef = vi.mocked(useFertilizerLogs).mock.calls[0][0]
    expect(idRef.value).toBe(1)
  })

  it("opens the view dialog for the selected log", async () => {
    const wrapper = mountComponent()

    const iconButtons = wrapper.findAll("button").filter((b) => !b.text())
    await iconButtons[0].trigger("click")
    await wrapper.vm.$nextTick()

    const viewDialog = wrapper.find('[data-test="view-dialog"]')
    expect(viewDialog.exists()).toBe(true)
    expect(viewDialog.attributes("data-open")).toBe("true")
  })

  it("opens the update dialog for the selected log", async () => {
    const wrapper = mountComponent()

    const iconButtons = wrapper.findAll("button").filter((b) => !b.text())
    await iconButtons[1].trigger("click")
    await wrapper.vm.$nextTick()

    const updateDialog = wrapper.findComponent({ name: "FertilizerLogUpdateDialog" })
    expect(updateDialog.exists()).toBe(true)
    expect(updateDialog.props("id")).toBe(1)
    expect(updateDialog.attributes("data-open")).toBe("true")
  })

  it("opens the create dialog when Add Entry is clicked", async () => {
    const wrapper = mountComponent()

    const addButton = wrapper.findAll("button").find((b) => b.text().includes("Add Entry"))
    await addButton?.trigger("click")
    await wrapper.vm.$nextTick()

    expect(wrapper.find('[data-test="create-dialog"]').attributes("data-open")).toBe("true")
  })

  it("calls onError when createLog rejects", async () => {
    mockCreateLog.mockRejectedValue(new Error("boom"))
    const wrapper = mountComponent()

    const onError = vi.fn()
    const payload = {
      logDate: "2024-03-01",
      eventType: "ADDED_WATER",
      itemAdded: "",
      quantity: "5 liters",
      notes: "",
    }
    await wrapper
      .findComponent({ name: "FertilizerLogCreateDialog" })
      .vm.$emit("submit", payload, onError)
    await flushPromises()

    expect(onError).toHaveBeenCalled()
  })

  it("calls updateLog when the update dialog emits submit", async () => {
    mockUpdateLog.mockResolvedValue(undefined)
    const wrapper = mountComponent()

    const iconButtons = wrapper.findAll("button").filter((b) => !b.text())
    await iconButtons[1].trigger("click")
    await wrapper.vm.$nextTick()

    const payload = {
      logDate: "2024-03-01",
      eventType: "STIRRED",
      itemAdded: "",
      quantity: "",
      notes: "",
    }
    await wrapper
      .findComponent({ name: "FertilizerLogUpdateDialog" })
      .vm.$emit("submit", 1, payload, vi.fn())
    await flushPromises()

    expect(mockUpdateLog).toHaveBeenCalledWith({ id: 1, payload })
  })

  it("calls onError when updateLog rejects", async () => {
    mockUpdateLog.mockRejectedValue(new Error("boom"))
    const wrapper = mountComponent()

    const iconButtons = wrapper.findAll("button").filter((b) => !b.text())
    await iconButtons[1].trigger("click")
    await wrapper.vm.$nextTick()

    const onError = vi.fn()
    const payload = {
      logDate: "2024-03-01",
      eventType: "STIRRED",
      itemAdded: "",
      quantity: "",
      notes: "",
    }
    await wrapper
      .findComponent({ name: "FertilizerLogUpdateDialog" })
      .vm.$emit("submit", 1, payload, onError)
    await flushPromises()

    expect(onError).toHaveBeenCalled()
  })

  it("advances to the next page", async () => {
    setupMock({ logs: ref({ results: defaultLogs.results, count: 25 }) })
    const wrapper = mountComponent()

    const nextButton = wrapper.findAll("button").find((b) => b.text() === "Next")
    await nextButton?.trigger("click")

    expect(wrapper.text()).toContain("Page 2 of 3")
  })

  it("goes back to the previous page", async () => {
    setupMock({ logs: ref({ results: defaultLogs.results, count: 25 }) })
    const wrapper = mountComponent()

    const nextButton = wrapper.findAll("button").find((b) => b.text() === "Next")
    await nextButton?.trigger("click")
    const previousButton = wrapper.findAll("button").find((b) => b.text() === "Previous")
    await previousButton?.trigger("click")

    expect(wrapper.text()).toContain("Page 1 of 3")
  })
})
