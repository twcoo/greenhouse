<script setup lang="ts">
import AppSidebar from "@/components/AppSidebar.vue"
import SiteHeader from "@/components/SiteHeader.vue"
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar"
</script>

<template>
  <SidebarProvider
    :style="{
      '--sidebar-width': 'calc(var(--spacing) * 72)',
      '--header-height': 'calc(var(--spacing) * 12)',
    }"
  >
    <AppSidebar variant="inset" />

    <SidebarInset>
      <SiteHeader />

      <div class="flex flex-col gap-4 py-4 md:gap-6 md:py-6 px-4 md:px-6">
        <slot />
      </div>
    </SidebarInset>
  </SidebarProvider>
</template>
