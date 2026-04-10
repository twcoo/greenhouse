import { mount } from "@vue/test-utils"
import { describe, it, expect } from "vitest"
import SiteHeader from "@/components/SiteHeader.vue"

describe("SiteHeader.vue", () => {
  const mountComponent = () => {
    return mount(SiteHeader, {
      global: {
        stubs: {
          SidebarTrigger: { template: "<div/>" },
          Separator: { template: "<div/>" },
        },
      },
    })
  }

  it("renders the header with a SidebarTrigger", () => {
    const wrapper = mountComponent()
    expect(wrapper.find("header").exists()).toBe(true)
    expect(wrapper.find('[data-test="sidebar-trigger"]').exists()).toBe(true)
  })

  it("contains a Separator component", () => {
    const wrapper = mountComponent()
    expect(wrapper.find('[data-test="separator"]').exists()).toBe(true)
  })
})
