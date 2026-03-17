import { mount } from "@vue/test-utils"
import { describe, it, expect, vi } from "vitest"
import SetupAdminForm from "@/components/SetupAdminForm.vue"
import { createTestingPinia } from "@pinia/testing"

const push = vi.fn()

vi.mock("vue-router", () => ({
  useRouter: () => ({
    push
  })
}))

const setupAdminMock = vi.fn()

vi.mock("@/composables/useSetup", () => ({
  useSetup: () => ({
    setupAdmin: setupAdminMock,
    loading: false
  })
}))

describe("SetupAdminForm.vue", () => {

  it("renders the form fields", () => {
    const wrapper = mount(SetupAdminForm, {
      global: {
        plugins: [createTestingPinia()]
      }
    })

    expect(wrapper.find("#username").exists()).toBe(true)
    expect(wrapper.find("#password").exists()).toBe(true)
    expect(wrapper.find("#password2").exists()).toBe(true)
  })

  it("shows validation errors when empty", async () => {
    const wrapper = mount(SetupAdminForm, {
      global: {
        plugins: [createTestingPinia()]
      }
    })

    await wrapper.find("form").trigger("submit.prevent")

    expect(wrapper.text()).toContain("characters")
  })

  it("calls setupAdmin when form is valid", async () => {
    const wrapper = mount(SetupAdminForm, {
      global: {
        plugins: [createTestingPinia()]
      }
    })

    await wrapper.find("#username").setValue("admin")
    await wrapper.find("#password").setValue("password123")
    await wrapper.find("#password2").setValue("password123")

    await wrapper.find("form").trigger("submit.prevent")

    expect(setupAdminMock).toHaveBeenCalled()
  })

  it("redirects to dashboard on success", async () => {
    setupAdminMock.mockResolvedValueOnce(undefined)

    const wrapper = mount(SetupAdminForm, {
      global: {
        plugins: [createTestingPinia()]
      }
    })

    await wrapper.find("#username").setValue("admin")
    await wrapper.find("#password").setValue("password123")
    await wrapper.find("#password2").setValue("password123")

    await wrapper.find("form").trigger("submit.prevent")

    expect(push).toHaveBeenCalledWith({ name: "dashboard" })
  })
})
