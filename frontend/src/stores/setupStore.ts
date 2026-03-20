import { defineStore } from "pinia"
import { ref } from "vue"
import { getStatus } from "@/api/services/setupService"

export const useSetupStore = defineStore("setup", () => {
  const setupRequired = ref(false)
  const setupChecked = ref(false)

  const checkSetup = async (): Promise<void> => {
    if (!setupChecked.value) {
      try {
        await getStatus()
        setupRequired.value = false
      } catch {
        setupRequired.value = true
      }

      setupChecked.value = true
    }
  }

  return { setupRequired, setupChecked, checkSetup }
})
