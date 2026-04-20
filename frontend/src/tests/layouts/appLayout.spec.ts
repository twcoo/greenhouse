import { describe, it, expect, vi } from "vitest"
import { mount } from "@vue/test-utils"
import AppLayout from "@/layouts/AppLayout.vue"

vi.mock("@/stores/authStore", () => ({
  useAuthStore: vi.fn(() => ({ user: null, logout: vi.fn() })),
}))

vi.mock("vue-router", () => ({
  useRouter: vi.fn(() => ({ push: vi.fn() })),
  RouterLink: { template: "<a><slot /></a>" },
}))

const stubs = {
  AppSidebar: { template: "<div data-stub='app-sidebar' />" },
  SiteHeader: { template: "<div data-stub='site-header' />" },
  SidebarProvider: { template: "<div><slot /></div>" },
  SidebarInset: { template: "<div><slot /></div>" },
}

describe("AppLayout", () => {
  it("renders the sidebar and header stubs", () => {
    const wrapper = mount(AppLayout, { global: { stubs } })

    expect(wrapper.find("[data-stub='app-sidebar']").exists()).toBe(true)
    expect(wrapper.find("[data-stub='site-header']").exists()).toBe(true)
  })

  it("renders slot content", () => {
    const wrapper = mount(AppLayout, {
      global: { stubs },
      slots: { default: "<p data-test='slot-content'>Page content</p>" },
    })

    expect(wrapper.find("[data-test='slot-content']").exists()).toBe(true)
    expect(wrapper.find("[data-test='slot-content']").text()).toBe("Page content")
  })
})
