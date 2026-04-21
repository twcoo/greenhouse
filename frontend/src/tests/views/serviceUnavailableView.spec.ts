import { describe, it, expect, vi, beforeEach } from "vitest"
import { mount } from "@vue/test-utils"
import { createTestingPinia } from "@pinia/testing"
import { useSetupStore } from "@/stores/setupStore"
import ServiceUnavailableView from "@/views/service-unavailable/index.vue"

const mockPush = vi.fn()

vi.mock("vue-router", async (importOriginal) => {
  const actual = await importOriginal<typeof import("vue-router")>()
  return {
    ...actual,
    useRouter: vi.fn(() => ({ push: mockPush })),
  }
})

const stubs = {
  IconHomeEco: { template: "<span />" },
  IconServerOff: { template: "<span />" },
}

function mountView() {
  return mount(ServiceUnavailableView, {
    global: {
      stubs,
      plugins: [createTestingPinia({ createSpy: vi.fn })],
    },
  })
}

beforeEach(() => {
  vi.clearAllMocks()
})

describe("ServiceUnavailableView", () => {
  it("renders the heading and message", () => {
    const wrapper = mountView()

    expect(wrapper.find("h1").text()).toBe("Unable to connect to the server")
    expect(wrapper.text()).toContain("We're having trouble reaching the server")
  })

  it("renders the Retry button", () => {
    const wrapper = mountView()

    expect(wrapper.find("button").text()).toBe("Retry")
  })

  it("calls retryConnection and navigates to / when Retry is clicked", async () => {
    const wrapper = mountView()
    const setupStore = useSetupStore()

    await wrapper.find("button").trigger("click")

    expect(setupStore.retryConnection).toHaveBeenCalled()
    expect(mockPush).toHaveBeenCalledWith("/")
  })
})
