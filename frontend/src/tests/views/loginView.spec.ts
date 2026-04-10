import { mount } from "@vue/test-utils"
import { describe, it, expect, vi } from "vitest"
import LoginView from "@/views/login/index.vue"
import LoginForm from "@/components/LoginForm.vue"
import { createTestingPinia } from "@pinia/testing"

describe("LoginView.vue", () => {
  const mountWithPinia = () =>
    mount(LoginView, {
      global: {
        plugins: [
          createTestingPinia({
            createSpy: vi.fn, // Tells Pinia to use Vitest for mocking actions
          }),
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
