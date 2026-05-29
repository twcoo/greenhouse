import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import LoginForm from "@/components/LoginForm.vue"
import { useAuthStore } from "@/stores/authStore"
import { createTestingPinia } from "@pinia/testing"
import { createAuthStoreMock } from "../../utils/test-utils"
import { mockPush } from "../../setup"

vi.mock("@/stores/authStore", () => ({
  useAuthStore: vi.fn(),
}))

beforeEach((): void => {
  vi.mocked(useAuthStore).mockReturnValue(
    createAuthStoreMock({
      isAuthenticated: false,
      user: null,
    }),
  )
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

    expect(wrapper.find('[data-test="usernameError"]').exists()).toBe(true)
    expect(wrapper.find('[data-test="passwordError"]').exists()).toBe(true)
  })

  it("calls login and redirects on success", async (): Promise<void> => {
    const storeMock = createAuthStoreMock({
      isAuthenticated: true,
    })
    vi.mocked(useAuthStore).mockReturnValue(storeMock)

    const wrapper = mountComponent()

    await wrapper.find('input[type="text"]').setValue("krubus")
    await wrapper.find('input[type="password"]').setValue("123456")

    await wrapper.find("form").trigger("submit.prevent")

    expect(storeMock.login).toHaveBeenCalledWith({
      username: "krubus",
      password: "123456",
    })
    expect(mockPush).toHaveBeenCalledWith({ name: "dashboard" })
  })

  it("displays general error from store", (): void => {
    vi.mocked(useAuthStore).mockReturnValueOnce(
      createAuthStoreMock({
        error: "Invalid credentials",
      }),
    )

    const wrapper = mountComponent()

    expect(wrapper.find('[data-test="general-error"]').text()).toContain("Invalid credentials")
  })

  describe("password visibility toggle", (): void => {
    it("password field defaults to type password", (): void => {
      const wrapper = mountComponent()

      expect((wrapper.get("#password").element as HTMLInputElement).type).toBe("password")
    })

    it("toggles password field to visible and back", async (): Promise<void> => {
      const wrapper = mountComponent()
      const toggleButton = wrapper.get('button[type="button"]')
      const passwordInput = wrapper.get("#password").element as HTMLInputElement

      await toggleButton.trigger("click")
      expect(passwordInput.type).toBe("text")

      await toggleButton.trigger("click")
      expect(passwordInput.type).toBe("password")
    })
  })

  it("disables button and shows loading state", (): void => {
    vi.mocked(useAuthStore).mockReturnValueOnce(
      createAuthStoreMock({
        isLoading: true,
      }),
    )

    const wrapper = mountComponent()

    const button = wrapper.find('button[type="submit"]')

    expect(button.attributes("disabled")).toBeDefined()
    expect(button.text()).toContain("Logging in...")
  })
})
