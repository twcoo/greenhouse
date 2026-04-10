import { mount } from "@vue/test-utils"
import { describe, it, expect, vi } from "vitest"
import LoginView from "@/views/login/index.vue"
import LoginForm from "@/components/LoginForm.vue"
import { createRouter, createWebHistory } from "vue-router"
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

describe("LoginView.vue", () => {
  const router = createRouter({
    history: createWebHistory(),
    routes: [{ path: "/login", component: { render: () => null } }],
  })

  const mountWithPinia = () =>
    mount(LoginView, {
      global: {
        plugins: [
          createTestingPinia({
            createSpy: vi.fn, // Tells Pinia to use Vitest for mocking actions
          }),
          router,
        ],
      },
    })

  it("renders the LoginForm component", () => {
    const wrapper = mountWithPinia()

    const formComponent = wrapper.findComponent(LoginForm)
    expect(formComponent.exists()).toBe(true)
  })

  it("passes necessary props to LoginForm if applicable", () => {
    const wrapper = mountWithPinia()
    const formComponent = wrapper.findComponent(LoginForm)

    expect(formComponent.isVisible()).toBe(true)
  })
})
