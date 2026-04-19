import { mount } from "@vue/test-utils"
import { describe, it, expect } from "vitest"
import DashboardView from "@/views/dashboard/index.vue"

describe("DashboardView", () => {
  it("renders the in-development message", () => {
    const wrapper = mount(DashboardView, {
      global: {
        stubs: {
          AppLayout: { template: "<div><slot /></div>" },
        },
      },
    })

    expect(wrapper.text()).toContain("In development")
  })
})
