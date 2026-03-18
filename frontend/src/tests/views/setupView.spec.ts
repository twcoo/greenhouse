import { mount } from "@vue/test-utils"
import { describe, it, expect, vi } from "vitest"
import SetupView from "@/views/setup/index.vue"
import SetupAdminForm from "@/components/SetupAdminForm.vue"
import { createTestingPinia } from "@pinia/testing"

vi.mock("vue-router", () => ({
  useRouter: () => ({
  }),
}))

const mountWithPinia = () =>
  mount(SetupView, {
    global: {
      plugins: [createTestingPinia()],
    },
  })

describe("SetupView.vue", () => {

  it("renders the SetupAdminForm component", () => {
    const wrapper = mountWithPinia()

    const formComponent = wrapper.findComponent(SetupAdminForm)
    expect(formComponent.exists()).toBe(true)
  })
})
