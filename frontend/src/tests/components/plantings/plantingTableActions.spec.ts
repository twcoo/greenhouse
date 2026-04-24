import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import PlantingTableActions from "@/components/plantings/PlantingTableActions.vue"
import type { Planting } from "@/types/planting"
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

const mockPlanting: Planting = {
  id: 1,
  crop: 1,
  cropName: "Tomato",
  variety: 1,
  varietyName: "Sun Gold",
  createdAt: "2024-01-01T00:00:00Z",
}

const mockUpdate = vi.fn()
const mockDelete = vi.fn()

const mountComponent = () =>
  mount(PlantingTableActions, {
    props: {
      row: { original: mockPlanting },
      table: {
        options: { meta: { update: mockUpdate, delete: mockDelete } },
      } as unknown as Table<Planting>,
    },
    global: { stubs },
  })

beforeEach(() => {
  vi.clearAllMocks()
})

describe("PlantingTableActions.vue", () => {
  it("calls table.options.meta.update when Update is clicked", async () => {
    const wrapper = mountComponent()

    const buttons = wrapper.findAll("button")
    const updateBtn = buttons.find((b) => b.text() === "Update")
    await updateBtn?.trigger("click")

    expect(mockUpdate).toHaveBeenCalledWith(mockPlanting.id, mockPlanting)
  })

  it("calls table.options.meta.delete when delete is confirmed", async () => {
    const wrapper = mountComponent()

    const buttons = wrapper.findAll("button")
    const deleteBtn = buttons.find((b) => b.text() === "Delete")
    await deleteBtn?.trigger("click")

    await wrapper.find("[data-testid='confirm-delete']").trigger("click")

    expect(mockDelete).toHaveBeenCalledWith(mockPlanting.id)
  })

  it("shows the variety name in the delete confirmation description", () => {
    const wrapper = mountComponent()
    expect(wrapper.text()).toContain("Sun Gold")
  })

  it("shows the crop name in the delete confirmation description", () => {
    const wrapper = mountComponent()
    expect(wrapper.text()).toContain("Tomato")
  })
})
