import { mount } from "@vue/test-utils"
import { describe, it, expect, vi } from "vitest"
import NavUser from "@/components/NavUser.vue"
import { createTestingPinia } from "@pinia/testing"

import { ref } from "vue"

// Mock useSidebar
vi.mock("@/components/ui/sidebar", async (importOriginal) => {
  const actual = await importOriginal<unknown>()
  return {
    ...actual,
    useSidebar: () => ({
      isMobile: ref(false),
    }),
  }
})

describe("NavUser.vue", () => {
  const mockUser = {
    username: "john.doe",
  }

  const mountComponent = (props = { user: mockUser }) => {
    return mount(NavUser, {
      props,
      global: {
        plugins: [createTestingPinia()],
        stubs: {
          DropdownMenu: { template: "<div><slot /></div>" },
          DropdownMenuTrigger: { template: "<div><slot /></div>" },
          DropdownMenuContent: { template: "<div><slot /></div>" },
          DropdownMenuItem: { template: "<div @click=\"$emit('click')\"><slot /></div>" },
          DropdownMenuLabel: { template: "<div><slot /></div>" },
          DropdownMenuSeparator: { template: "<div />" },
          SidebarMenu: { template: "<div><slot /></div>" },
          SidebarMenuItem: { template: "<div><slot /></div>" },
          SidebarMenuButton: { template: "<div><slot /></div>" },
          Avatar: { template: "<div><slot /></div>" },
          AvatarFallback: { template: "<div><slot /></div>" },
          IconDotsVertical: { template: "<svg />" },
          IconLogout: { template: "<svg />" },
        },
      },
    })
  }

  it("renders the username correctly", () => {
    const wrapper = mountComponent()

    // Check if username appears in the component
    // It appears twice: once in the sidebar button and once in the dropdown label
    const usernameElements = wrapper.findAll(".truncate.font-medium")
    expect(usernameElements).toHaveLength(2)
    expect(usernameElements[0].text()).toBe(mockUser.username)
    expect(usernameElements[1].text()).toBe(mockUser.username)
  })

  it("calculates initials correctly for 'John Doe'", () => {
    const wrapper = mountComponent({
      user: { username: "John Doe" },
    })

    const avatarFallback = wrapper.get('[data-test="avatar-fallback"]')

    expect(avatarFallback.text()).toBe("JD")
    const avatarFallbackMobile = wrapper.get('[data-test="avatar-fallback-mobile"]')
    expect(avatarFallbackMobile.text()).toBe("JD")
  })

  it("emits 'logout' event when logout item is clicked", async () => {
    const wrapper = mountComponent()

    const logoutItem = wrapper.get('[data-test="logout"]')
    await logoutItem.trigger("select")

    const logoutEvent = wrapper.emitted("logout")
    expect(logoutEvent).toBeTruthy()
    expect(logoutEvent).toHaveLength(1)
  })
})
