import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import AppSidebar from "@/components/AppSidebar.vue"
import { createTestingPinia } from "@pinia/testing"
import { useAuthStore } from "@/stores/authStore"

const push = vi.fn()
let logoutMock: ReturnType<typeof vi.fn>

const createAuthStoreMock = (overrides = {}): ReturnType<typeof useAuthStore> =>
  ({
    user: { username: "krubus" },
    logout: logoutMock,
    isAuthenticated: true,
    isLoading: false,
    error: null,
    login: vi.fn(),
    clearAuth: vi.fn(),
    ...overrides,
  }) as unknown as ReturnType<typeof useAuthStore>

vi.mock("vue-router", () => ({
  useRouter: () => ({
    push,
  }),
}))

vi.mock("@/stores/authStore", () => ({
  useAuthStore: vi.fn(),
}))

beforeEach(() => {
  logoutMock = vi.fn().mockResolvedValue(undefined)

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

    expect(logoutMock).toHaveBeenCalled()
    expect(push).toHaveBeenCalledWith({ name: "login" })
  })

  it("passes correct navMain items to NavMain", (): void => {
    const wrapper = mountComponent()

    const navMain = wrapper.findComponent({ name: "NavMain" })

    const items = navMain.props("items")

    expect(items).toHaveLength(3)

    expect(items).toEqual([
      expect.objectContaining({
        title: "Dashboard",
        url: "#",
      }),
      expect.objectContaining({
        title: "Crops",
        url: "#",
      }),
      expect.objectContaining({
        title: "Planting Locations",
        url: "#",
      }),
    ])
  })
})
