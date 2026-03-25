<script setup lang="ts">
import LoginForm from "@/components/LoginForm.vue"
import { IconHomeEco } from "@tabler/icons-vue"
</script>

<template>
  <div class="bg-muted flex min-h-svh flex-col items-center justify-center gap-6 p-6 md:p-10">
    <div class="flex w-full max-w-sm flex-col gap-6">
      <a href="#" class="flex items-center gap-2 self-center font-medium">
        <div
          class="bg-primary text-primary-foreground flex size-6 items-center justify-center rounded-md"
        >
          <IconHomeEco class="!size-5" />
        </div>
        Greenhouse
      </a>
      <LoginForm />
    </div>
  </div>
</template>
