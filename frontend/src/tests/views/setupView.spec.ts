import { mount } from "@vue/test-utils"
import { describe, it, expect, vi } from "vitest"
import SetupView from "@/views/setup/index.vue"
import SetupAdminForm from "@/components/SetupAdminForm.vue"
import { createRouter, createWebHistory } from "vue-router" // Added these back
import { createTestingPinia } from "@pinia/testing"

vi.mock("vue-router", async (importOriginal) => {
  const actual = await importOriginal<typeof import("vue-router")>()
  return {
    ...actual,
    useRouter: () => ({
      push: vi.fn(),
      replace: vi.fn(),
    }),
    useRoute: () => ({
      params: {},
      query: {},
    }),
  }
})

describe("SetupView.vue", () => {
  const router = createRouter({
    history: createWebHistory(),
    routes: [{ path: "/setup", component: { render: () => null } }],
  })

  const mountWithPinia = () =>
    mount(SetupView, {
      global: {
        plugins: [
          createTestingPinia({
            createSpy: vi.fn, // Automatically mock pinia actions with Vitest spies
          }),
          router,
        ],
      },
    })

  it("renders the SetupAdminForm component", () => {
    const wrapper = mountWithPinia()

    const formComponent = wrapper.findComponent(SetupAdminForm)
    expect(formComponent.exists()).toBe(true)
  })
})
