import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import FertilizerTableActions from "@/components/fertilizers/FertilizerTableActions.vue"
import type { Fertilizer } from "@/types/fertilizer"
import type { Table } from "@tanstack/vue-table"

const stubs = {
  DropdownMenu: { template: "<div><slot /></div>" },
  DropdownMenuTrigger: { template: "<div><slot /></div>" },
  DropdownMenuContent: { template: "<div><slot /></div>" },
  DropdownMenuLabel: { template: "<div><slot /></div>" },
  DropdownMenuItem: { template: "<button v-bind='$attrs'><slot /></button>" },
  DropdownMenuSeparator: { template: "<hr />" },
  AlertDialog: { template: "<div><slot /></div>", props: ["open"] },
  AlertDialogContent: { template: "<div><slot /></div>" },
  AlertDialogHeader: { template: "<div><slot /></div>" },
  AlertDialogTitle: { template: "<div><slot /></div>" },
  AlertDialogDescription: { template: "<div><slot /></div>" },
  AlertDialogFooter: { template: "<div><slot /></div>" },
  AlertDialogAction: {
    template: "<button v-bind='$attrs' data-testid='confirm-delete'><slot /></button>",
  },
  AlertDialogCancel: { template: "<button><slot /></button>" },
  Button: { template: "<button><slot /></button>" },
  MoreHorizontal: { template: "<svg />" },
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

const mockUpdate = vi.fn()
const mockDelete = vi.fn()
const mockAction = vi.fn()

const mountComponent = () =>
  mount(FertilizerTableActions, {
    props: {
      row: { original: mockFertilizer },
      table: {
        options: { meta: { update: mockUpdate, delete: mockDelete, action: mockAction } },
      } as unknown as Table<Fertilizer>,
    },
    global: { stubs },
  })

beforeEach(() => {
  vi.clearAllMocks()
})

describe("FertilizerTableActions.vue", () => {
  it("calls table.options.meta.update when Update is clicked", async () => {
    const wrapper = mountComponent()

    const buttons = wrapper.findAll("button")
    const updateBtn = buttons.find((b) => b.text() === "Update")
    await updateBtn?.trigger("click")

    expect(mockUpdate).toHaveBeenCalledWith(mockFertilizer.id, mockFertilizer)
  })

  it("calls table.options.meta.action with manage-logs when Logs is clicked", async () => {
    const wrapper = mountComponent()

    const buttons = wrapper.findAll("button")
    const logsBtn = buttons.find((b) => b.text() === "Logs")
    await logsBtn?.trigger("click")

    expect(mockAction).toHaveBeenCalledWith("manage-logs", mockFertilizer.id)
  })

  it("calls table.options.meta.delete when delete is confirmed", async () => {
    const wrapper = mountComponent()

    const buttons = wrapper.findAll("button")
    const deleteBtn = buttons.find((b) => b.text() === "Delete")
    await deleteBtn?.trigger("click")

    await wrapper.find("[data-testid='confirm-delete']").trigger("click")

    expect(mockDelete).toHaveBeenCalledWith(mockFertilizer.id)
  })

  it("shows the fertilizer name in the delete confirmation description", () => {
    const wrapper = mountComponent()

    expect(wrapper.text()).toContain(mockFertilizer.name)
  })
})
