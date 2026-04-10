import { mount } from "@vue/test-utils"
import { describe, it, expect, vi } from "vitest"
import SetupView from "@/views/setup/index.vue"
import SetupAdminForm from "@/components/SetupAdminForm.vue"
import { createTestingPinia } from "@pinia/testing"

describe("SetupView.vue", () => {
  const mountWithPinia = () =>
    mount(SetupView, {
      global: {
        plugins: [
          createTestingPinia({
            createSpy: vi.fn, // Automatically mock pinia actions with Vitest spies
          }),
        ],
      },
    })

  it("renders the SetupAdminForm component", () => {
    const wrapper = mountWithPinia()

    const formComponent = wrapper.findComponent(SetupAdminForm)
    expect(formComponent.exists()).toBe(true)
  })
})
