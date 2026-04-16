<script setup lang="ts">
import { IconDashboard, IconPlant, IconMap2, IconHomeEco, IconSeeding } from "@tabler/icons-vue"

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
import { useRouter } from "vue-router"

const router = useRouter()
const authStore = useAuthStore()

const data = {
  navMain: [
    {
      title: "Dashboard",
      to: { name: "dashboard" },
      icon: IconDashboard,
    },
    {
      title: "Crops",
      to: { name: "crops" },
      icon: IconPlant,
    },
    {
      title: "Planting Locations",
      to: { name: "planting-locations" },
      icon: IconMap2,
    },
    {
      title: "Varieties",
      to: { name: "varieties" },
      icon: IconSeeding,
    },
  ],
}

const handleLogout = async (): Promise<void> => {
  await authStore.logout()
  await router.push({ name: "login" })
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
      <NavUser v-if="authStore.user" :user="authStore.user" @logout="handleLogout" />
    </SidebarFooter>
  </Sidebar>
</template>
