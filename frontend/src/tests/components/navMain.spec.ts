import { mount, RouterLinkStub } from "@vue/test-utils"
import { describe, it, expect, } from "vitest"
import NavMain from "@/components/NavMain.vue"
import { defineComponent, h } from "vue"

const MockIcon = defineComponent({
  name: "MockIcon",
  render() {
    return h("svg", { "data-test": "nav-icon" })
  },
})

describe("NavMain.vue", () => {
  const mockItems = [
    {
      title: "Dashboard",
      to: { name: "dashboard" },
      icon: MockIcon,
    },
    {
      title: "Crops",
      to: "/crops",
    },
  ]

  const mountComponent = (props = { items: mockItems }) => {
    return mount(NavMain, {
      props,
      global: {
        stubs: {
          SidebarGroup: { template: "<div><slot /></div>" },
          SidebarGroupContent: { template: "<div><slot /></div>" },
          SidebarMenu: { template: "<div><slot /></div>" },
          SidebarMenuItem: { template: "<div><slot /></div>" },
          SidebarMenuButton: { template: "<div><slot /></div>" },
          RouterLink: RouterLinkStub,
        },
      },
    })
  }

  it("renders the correct number of navigation items", () => {
    const wrapper = mountComponent()
    const items = wrapper.findAllComponents(RouterLinkStub)
    expect(items).toHaveLength(mockItems.length)
  })

  it("renders titles for each navigation item", () => {
    const wrapper = mountComponent()
    const text = wrapper.text()

    mockItems.forEach(item => {
      expect(text).toContain(item.title)
    })
  })

  it("sets the correct 'to' prop for router-links", () => {
    const wrapper = mountComponent()
    const links = wrapper.findAllComponents(RouterLinkStub)

    expect(links[0].props("to")).toEqual(mockItems[0].to)
    expect(links[1].props("to")).toBe(mockItems[1].to)
  })

  it("renders icon when provided", () => {
    const wrapper = mountComponent()
    const icons = wrapper.findAll('[data-test="nav-icon"]')

    expect(icons).toHaveLength(1)
  })

  it("does not render icon when not provided", () => {
    const wrapper = mountComponent({
      items: [
        { title: "No Icon", to: "/no-icon" }
      ]
    })

    const icons = wrapper.findAll('[data-test="nav-icon"]')
    expect(icons).toHaveLength(0)
  })
})
