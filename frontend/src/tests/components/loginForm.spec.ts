import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import LoginForm from "@/components/LoginForm.vue"
import { useAuthStore } from "@/stores/authStore"
import { createTestingPinia } from "@pinia/testing"

const push = vi.fn()

vi.mock("vue-router", () => ({
  useRouter: () => ({ push }),
}))

vi.mock("@/stores/authStore", () => ({
  useAuthStore: vi.fn(),
}))

let loginMock: ReturnType<typeof vi.fn>

const createAuthStoreMock = (overrides = {}) => ({
  login: loginMock,
  isAuthenticated: false,
  loading: false,
  error: "",
  ...overrides,
})

beforeEach((): void => {
  loginMock = vi.fn()

  vi.mocked(useAuthStore).mockReturnValue(
    createAuthStoreMock()
  )

  push.mockClear()
})

const mountComponent = () =>
  mount(LoginForm, {
    global: {
      plugins: [createTestingPinia()],
    },
  })

describe("LoginForm.vue", (): void => {
  it("renders login form", (): void => {
    const wrapper = mountComponent()

    expect(wrapper.find('input[type="text"]').exists()).toBe(true)
    expect(wrapper.find('input[type="password"]').exists()).toBe(true)
    expect(wrapper.find("button").exists()).toBe(true)
  })

  it("shows validation errors when fields are empty", async (): Promise<void> => {
    const wrapper = mountComponent()

    await wrapper.find("form").trigger("submit.prevent")

    expect(wrapper.find('[data-test="username-error"]').exists()).toBe(true)
    expect(wrapper.find('[data-test="password-error"]').exists()).toBe(true)
  })

  it("calls login and redirects on success", async (): Promise<void> => {
    vi.mocked(useAuthStore).mockReturnValueOnce(
      createAuthStoreMock({
        isAuthenticated: true,
      })
    )

    const wrapper = mountComponent()

    await wrapper.find('input[type="text"]').setValue("krubus")
    await wrapper.find('input[type="password"]').setValue("123456")

    await wrapper.find("form").trigger("submit.prevent")

    expect(loginMock).toHaveBeenCalledWith({
      username: "krubus",
      password: "123456",
    })

    expect(push).toHaveBeenCalledWith({ name: "dashboard" })
  })

  it("displays general error from store", (): void => {
    vi.mocked(useAuthStore).mockReturnValueOnce(
      createAuthStoreMock({
        error: "Invalid credentials",
      })
    )

    const wrapper = mountComponent()

    expect(wrapper.find('[data-test="general-error"]').text())
      .toContain("Invalid credentials")
  })

  it("disables button and shows loading state", (): void => {
    vi.mocked(useAuthStore).mockReturnValueOnce(
      createAuthStoreMock({
        loading: true,
      })
    )

    const wrapper = mountComponent()

    const button = wrapper.find("button")

    expect(button.attributes("disabled")).toBeDefined()
    expect(button.text()).toContain("Logging in...")
  })
})
