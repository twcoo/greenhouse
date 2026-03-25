import { mount } from "@vue/test-utils"
import { describe, it, expect, vi } from "vitest"
import LoginView from "@/views/login/index.vue"
import LoginForm from "@/components/LoginForm.vue"
import { createTestingPinia } from "@pinia/testing"

vi.mock("vue-router", () => ({
  useRouter: () => ({}),
}))

const mountWithPinia = () =>
  mount(LoginView, {
    global: {
      plugins: [createTestingPinia()],
    },
  })

describe("LoginView.vue", () => {
  it("renders the LoginForm component", () => {
    const wrapper = mountWithPinia()

    const formComponent = wrapper.findComponent(LoginForm)
    expect(formComponent.exists()).toBe(true)
  })
})
