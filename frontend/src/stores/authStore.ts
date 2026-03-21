import { defineStore } from "pinia"
import { ref } from "vue"
import { User } from "@/types/user"
import { authLogin, authLogout } from "@/api/services/authService"
import type { authLoginPayload } from "@/types/auth"

export const useAuthStore = defineStore("setup", () => {
  const user = ref<User | null>(null)
  const isAuthenticated = ref(false)
  const isLoading = ref<boolean>(false)
  const error = ref<string | null>(null)

  const login = async (payload: authLoginPayload): Promise<void> => {
    isLoading.value = true
    error.value = null

    try {
      const data = await authLogin(payload)

      user.value = data.user
      isAuthenticated.value = true
    } catch {
      user.value = null
      isAuthenticated.value = false
    } finally {
      isLoading.value = false
    }
  }

  const logout = async (): Promise<void> => {
    try {
      await authLogout()

      user.value = null
      isAuthenticated.value = false
    } catch {
      user.value = null
      isAuthenticated.value = false
    }
  }

  return { user, isAuthenticated, isLoading, error, login, logout }
})
