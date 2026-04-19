import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import AppSidebar from "@/components/AppSidebar.vue"
import { createTestingPinia } from "@pinia/testing"
import { useAuthStore } from "@/stores/authStore"
import { IconDashboard, IconPlant, IconMap2, IconSeeding } from "@tabler/icons-vue"
import { createAuthStoreMock } from "../utils/test-utils"
import { mockPush } from "../setup"

vi.mock("@/stores/authStore", () => ({
  useAuthStore: vi.fn(),
}))

beforeEach(() => {
  vi.mocked(useAuthStore).mockReturnValue(createAuthStoreMock())
})

const mountComponent = () =>
  mount(AppSidebar, {
    global: {
      plugins: [createTestingPinia()],
      stubs: {
        Sidebar: { template: "<div><slot /></div>" },
        SidebarMenuButton: true,
        NavUser: true,
      },
    },
  })

describe("AppSidebar.vue", () => {
  it("renders sidebar with main nav and user section", (): void => {
    const wrapper = mountComponent()

    expect(wrapper.findComponent({ name: "NavMain" }).exists()).toBe(true)
    expect(wrapper.findComponent({ name: "NavUser" }).exists()).toBe(true)
  })

  it("does not show NavUser when no user is logged in", (): void => {
    vi.mocked(useAuthStore).mockReturnValueOnce(
      createAuthStoreMock({
        user: null,
      }),
    )

    const wrapper = mountComponent()

    expect(wrapper.findComponent({ name: "NavUser" }).exists()).toBe(false)
  })

  it("calls logout and redirects on logout button click", async (): Promise<void> => {
    const wrapper = mountComponent()

    await wrapper.findComponent({ name: "NavUser" }).vm.$emit("logout")

    expect(vi.mocked(useAuthStore)().logout).toHaveBeenCalled()
    expect(mockPush).toHaveBeenCalledWith({ name: "login" })
  })

  it("passes correct navMain items to NavMain", (): void => {
    const wrapper = mountComponent()

    const navMain = wrapper.findComponent({ name: "NavMain" })

    const items = navMain.props("items")

    expect(items).toHaveLength(4)

    expect(items).toEqual([
      expect.objectContaining({
        title: "Dashboard",
        to: { name: "dashboard" },
        icon: IconDashboard,
      }),
      expect.objectContaining({
        title: "Crops",
        to: { name: "crops" },
        icon: IconPlant,
      }),
      expect.objectContaining({
        title: "Planting Locations",
        to: { name: "planting-locations" },
        icon: IconMap2,
      }),
      expect.objectContaining({
        title: "Varieties",
        to: { name: "varieties" },
        icon: IconSeeding,
      }),
    ])
  })
})
