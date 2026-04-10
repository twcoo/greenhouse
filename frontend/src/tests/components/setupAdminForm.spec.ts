import { mount } from "@vue/test-utils"
import { describe, it, expect, vi, beforeEach } from "vitest"
import SetupAdminForm from "@/components/SetupAdminForm.vue"
import { createRouter, createWebHistory } from "vue-router"
import { createTestingPinia } from "@pinia/testing"

const push = vi.fn()
const setupAdminMock = vi.fn()
const loadingMock = vi.fn(() => false)

vi.mock("vue-router", async (importOriginal) => {
  const actual = await importOriginal<typeof import("vue-router")>()
  return {
    ...actual,
    useRouter: () => ({
      push,
    }),
  }
})

vi.mock("@/composables/useSetup", () => ({
  useSetup: () => ({
    setupAdmin: setupAdminMock,
    get loading() {
      return loadingMock()
    },
  }),
}))

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/setup", component: { render: () => null } },
    { path: "/dashboard", name: "dashboard", component: { render: () => null } },
  ],
})

const mountComponent = () =>
  mount(SetupAdminForm, {
    global: {
      plugins: [
        createTestingPinia({
          createSpy: vi.fn,
        }),
        router,
      ],
    },
  })

beforeEach((): void => {
  vi.clearAllMocks()
  loadingMock.mockReturnValue(false)
  push.mockClear()
})

describe("SetupAdminForm.vue", (): void => {
  it("renders form fields", (): void => {
    const wrapper = mountComponent()

    expect(wrapper.find("#username").exists()).toBe(true)
    expect(wrapper.find("#password").exists()).toBe(true)
    expect(wrapper.find("#password2").exists()).toBe(true)
  })

  it("shows validation errors on empty submit", async (): Promise<void> => {
    const wrapper = mountComponent()

    await wrapper.get("form").trigger("submit.prevent")

    const usernameError = wrapper.get('[data-test="username-error"]')
    const passwordError = wrapper.get('[data-test="password-error"]')

    expect(usernameError.text().trim()).toBe("Username must be at least 3 characters")
    expect(passwordError.text().trim()).toBe("Password must be at least 8 characters")
  })

  it("displays error when password and confirmation do not match", async (): Promise<void> => {
    const wrapper = mountComponent()

    await wrapper.get("#username").setValue("admin")
    await wrapper.get("#password").setValue("password123")
    await wrapper.get("#password2").setValue("iamdifferent")

    await wrapper.get("form").trigger("submit.prevent")

    const confirmPasswordError = wrapper.get('[data-test="password2-error"]')

    expect(confirmPasswordError.text().trim()).toBe("Password do not match")
  })

  it("allows user to fill the form", async (): Promise<void> => {
    const wrapper = mountComponent()

    await wrapper.get("#username").setValue("admin")
    await wrapper.get("#password").setValue("password123")
    await wrapper.get("#password2").setValue("password123")

    expect((wrapper.get("#username").element as HTMLInputElement).value).toBe("admin")
    expect((wrapper.get("#password").element as HTMLInputElement).value).toBe("password123")
    expect((wrapper.get("#password2").element as HTMLInputElement).value).toBe("password123")
  })

  it("shows general error when no API response", async (): Promise<void> => {
    setupAdminMock.mockRejectedValueOnce(new Error("Network error"))

    const wrapper = mountComponent()

    await wrapper.get("#username").setValue("admin")
    await wrapper.get("#password").setValue("password123")
    await wrapper.get("#password2").setValue("password123")

    await wrapper.get("form").trigger("submit.prevent")

    const generalError = wrapper.get('[data-test="general-error"]')

    expect(generalError.text().trim()).toBe("Something went wrong. Please try again.")
  })

  it("disables button and shows loading text when loading", async (): Promise<void> => {
    loadingMock.mockReturnValue(true)

    const wrapper = mountComponent()

    const button = wrapper.get("button")

    expect(button.attributes("disabled")).toBeDefined()
    expect(button.text()).toBe("Creating...")
  })

  it("submits and redirects on success", async (): Promise<void> => {
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
