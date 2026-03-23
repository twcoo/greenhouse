<script setup lang="ts">
import { IconDashboard, IconPlant, IconMap2, IconHomeEco } from "@tabler/icons-vue"

import NavMain from "@/components/NavMain.vue"
import NavUser from "@/components/NavUser.vue"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"
import { useAuthStore } from "@/stores/authStore"

const authStore = useAuthStore()

const data = {
  navMain: [
    {
      title: "Dashboard",
      url: "#",
      icon: IconDashboard,
    },
    {
      title: "Crops",
      url: "#",
      icon: IconPlant,
    },
    {
      title: "Planting Locations",
      url: "#",
      icon: IconMap2,
    },
  ],
}
</script>

<template>
  <Sidebar collapsible="offcanvas">
    <SidebarHeader>
      <SidebarMenu>
        <SidebarMenuItem>
          <SidebarMenuButton as-child class="data-[slot=sidebar-menu-button]:!p-1.5">
            <a href="#">
              <IconHomeEco class="!size-5" />
              <span class="text-base font-semibold">Greenhouse</span>
            </a>
          </SidebarMenuButton>
        </SidebarMenuItem>
      </SidebarMenu>
    </SidebarHeader>
    <SidebarContent>
      <NavMain :items="data.navMain" />
    </SidebarContent>
    <SidebarFooter>
      <NavUser :user="authStore.user" />
    </SidebarFooter>
  </Sidebar>
</template>
