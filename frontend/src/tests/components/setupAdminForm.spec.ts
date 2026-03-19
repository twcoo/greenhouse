import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import SetupAdminForm from "@/components/SetupAdminForm.vue"
import { createTestingPinia } from "@pinia/testing"

const push = vi.fn()
const setupAdminMock = vi.fn()
const loadingMock = vi.fn(() => false)

vi.mock("vue-router", () => ({
  useRouter: () => ({
    push,
  }),
}))

vi.mock("@/composables/useSetup", () => ({
  useSetup: () => ({
    setupAdmin: setupAdminMock,
    get loading() {
      return loadingMock()
    },
  }),
}))

const mountComponent = () =>
  mount(SetupAdminForm, {
    global: {
      plugins: [createTestingPinia()],
    },
  })

beforeEach(() => {
  vi.clearAllMocks()
  loadingMock.mockReturnValue(false)
})

describe("SetupAdminForm.vue", () => {
  it("renders form fields", () => {
    const wrapper = mountComponent()

    expect(wrapper.get("#username").exists()).toBe(true)
    expect(wrapper.get("#password").exists()).toBe(true)
    expect(wrapper.get("#password2").exists()).toBe(true)
  })

  it("shows validation errors on empty submit", async () => {
    const wrapper = mountComponent()

    await wrapper.get("form").trigger("submit.prevent")

    const usernameError = wrapper.get('[data-test="username-error"]')
    const passwordError = wrapper.get('[data-test="password-error"]')

    expect(usernameError.text().trim()).toBe("Username must be at least 3 characters")
    expect(passwordError.text().trim()).toBe("Password must be at least 8 characters")
  })

  it("displays error when password and confirmation do not match", async () => {
    const wrapper = mountComponent()

    await wrapper.get("#username").setValue("admin")
    await wrapper.get("#password").setValue("password123")
    await wrapper.get("#password2").setValue("iamdifferent")

    await wrapper.get("form").trigger("submit.prevent")

    const confirmPasswordError = wrapper.get('[data-test="password2-error"]')

    expect(confirmPasswordError.text().trim()).toBe("Password do not match")
  })

  it("allows user to fill the form", async () => {
    const wrapper = mountComponent()

    await wrapper.get("#username").setValue("admin")
    await wrapper.get("#password").setValue("password123")
    await wrapper.get("#password2").setValue("password123")

    expect((wrapper.get("#username").element as HTMLInputElement).value).toBe("admin")
    expect((wrapper.get("#password").element as HTMLInputElement).value).toBe("password123")
    expect((wrapper.get("#password2").element as HTMLInputElement).value).toBe("password123")
  })

  it("shows general error when no API response", async () => {
    setupAdminMock.mockRejectedValueOnce(new Error("Network error"))

    const wrapper = mountComponent()

    await wrapper.get("#username").setValue("admin")
    await wrapper.get("#password").setValue("password123")
    await wrapper.get("#password2").setValue("password123")

    await wrapper.get("form").trigger("submit.prevent")

    const generalError = wrapper.get('[data-test="general-error"]')

    expect(generalError.text().trim()).toBe("Something went wrong. Please try again.")
  })

  it("disables button and shows loading text when loading", async () => {
    loadingMock.mockReturnValue(true)

    const wrapper = mountComponent()

    const button = wrapper.get("button")

    expect(button.attributes("disabled")).toBeDefined()
    expect(button.text()).toBe("Creating...")
  })

  it("submits and redirects on success", async () => {
    setupAdminMock.mockResolvedValueOnce(undefined)

    const wrapper = mountComponent()

    await wrapper.get("#username").setValue("admin")
    await wrapper.get("#password").setValue("password123")
    await wrapper.get("#password2").setValue("password123")

    await wrapper.get("form").trigger("submit.prevent")

    expect(setupAdminMock).toHaveBeenCalledWith({
      username: "admin",
      password: "password123",
      password2: "password123",
    })

    expect(push).toHaveBeenCalledWith({ name: "dashboard" })
  })
})
