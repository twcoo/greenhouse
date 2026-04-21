<script setup lang="ts">
import { IconHomeEco, IconServerOff } from "@tabler/icons-vue"
import { useRouter } from "vue-router"
import { useSetupStore } from "@/stores/setupStore"

const router = useRouter()
const setupStore = useSetupStore()

const retry = async (): Promise<void> => {
  setupStore.retryConnection()
  await router.push("/")
}
</script>

<template>
  <div class="bg-muted flex min-h-svh flex-col items-center justify-center gap-6 p-6 md:p-10">
    <div class="flex w-full max-w-sm flex-col items-center gap-6 text-center">
      <a href="#" class="flex items-center gap-2 self-center font-medium">
        <div
          class="bg-primary text-primary-foreground flex size-6 items-center justify-center rounded-md"
        >
          <IconHomeEco class="!size-5" />
        </div>
        Greenhouse
      </a>

      <div class="flex flex-col items-center gap-3">
        <IconServerOff class="text-muted-foreground size-12" />
        <h1 class="text-xl font-semibold">Unable to connect to the server</h1>
        <p class="text-muted-foreground text-sm">
          We're having trouble reaching the server. Please make sure the application is running and
          try again.
        </p>
      </div>

      <button
        class="bg-primary text-primary-foreground hover:bg-primary/90 w-full rounded-md px-4 py-2 text-sm font-medium transition-colors"
        @click="retry"
      >
        Retry
      </button>
    </div>
  </div>
</template>
