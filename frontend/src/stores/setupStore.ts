import axios from "axios"
import { defineStore } from "pinia"
import { ref } from "vue"
import { getStatus } from "@/api/services/setupService"

export const useSetupStore = defineStore("setup", () => {
  const setupRequired = ref(false)
  const setupChecked = ref(false)
  const backendUnavailable = ref(false)

  const checkSetup = async (): Promise<void> => {
    if (setupChecked.value) return

    try {
      await getStatus()
      setupRequired.value = false
    } catch (error) {
      if (axios.isAxiosError(error) && !error.response) {
        backendUnavailable.value = true
      } else {
        setupRequired.value = true
      }
    } finally {
      setupChecked.value = true
    }
  }

  const retryConnection = (): void => {
    setupChecked.value = false
    backendUnavailable.value = false
  }

  return { setupRequired, setupChecked, backendUnavailable, checkSetup, retryConnection }
})
