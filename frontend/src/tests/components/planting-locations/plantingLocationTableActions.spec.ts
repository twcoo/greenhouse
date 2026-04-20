import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import PlantingLocationTableActions from "@/components/planting-locations/PlantingLocationTableActions.vue"
import type { PlantingLocation } from "@/types/plantingLocation"
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
  AlertDialogAction: { template: "<button v-bind='$attrs' data-testid='confirm-delete'><slot /></button>" },
  AlertDialogCancel: { template: "<button><slot /></button>" },
  Button: { template: "<button><slot /></button>" },
  MoreHorizontal: { template: "<svg />" },
}

const mockLocation: PlantingLocation = {
  id: 1,
  name: "Garden Pot",
  locationType: "POT",
  width: 30,
  height: 40,
}

const mockUpdate = vi.fn()
const mockDelete = vi.fn()

const mountComponent = () =>
  mount(PlantingLocationTableActions, {
    props: {
      row: { original: mockLocation },
      table: {
        options: { meta: { update: mockUpdate, delete: mockDelete } },
      } as unknown as Table<PlantingLocation>,
    },
    global: { stubs },
  })

beforeEach(() => {
  vi.clearAllMocks()
})

describe("PlantingLocationTableActions.vue", () => {
  it("calls table.options.meta.update when Update is clicked", async () => {
    const wrapper = mountComponent()

    const buttons = wrapper.findAll("button")
    const updateBtn = buttons.find((b) => b.text() === "Update")
    await updateBtn?.trigger("click")

    expect(mockUpdate).toHaveBeenCalledWith(mockLocation.id, mockLocation)
  })

  it("calls table.options.meta.delete when delete is confirmed", async () => {
    const wrapper = mountComponent()

    const buttons = wrapper.findAll("button")
    const deleteBtn = buttons.find((b) => b.text() === "Delete")
    await deleteBtn?.trigger("click")

    await wrapper.find("[data-testid='confirm-delete']").trigger("click")

    expect(mockDelete).toHaveBeenCalledWith(mockLocation.id)
  })

  it("shows the location name in the delete confirmation description", () => {
    const wrapper = mountComponent()

    expect(wrapper.text()).toContain(mockLocation.name)
  })
})
