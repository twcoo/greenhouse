import { defineStore } from "pinia"
import { ref } from "vue"
import { useStorage } from "@vueuse/core"
import type { User } from "@/types/user"
import type { authLoginPayload } from "@/types/auth"
import type { AxiosError } from "axios"
import type { APIErrorResponse } from "@/types/api"
import { useCookies } from "@vueuse/integrations/useCookies"
import { authLogin, authLogout } from "@/api/services/authService"

export const useAuthStore = defineStore("auth", () => {
  const cookies = useCookies(["csrftoken", "token"])
  const user = useStorage<User | null>("user", null, localStorage, {
    serializer: {
      read: (v: string) => (v ? JSON.parse(v) : null),
      write: (v: User | null) => JSON.stringify(v),
    },
  })
  const isAuthenticated = useStorage<boolean>("isAuthenticated", false)
  const isLoading = ref<boolean>(false)
  const error = ref<string | null>(null)

  const login = async (payload: authLoginPayload): Promise<void> => {
    isLoading.value = true
    error.value = null

    try {
      const data = await authLogin(payload)

      user.value = data.user
      isAuthenticated.value = true
    } catch (err) {
      user.value = null
      isAuthenticated.value = false

      const axiosError = err as AxiosError<APIErrorResponse>

      error.value = axiosError.response?.data
        ? String(axiosError.response.data.message)
        : "Something went wrong. Please try again."
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

  const clearAuth = () => {
    user.value = null
    isAuthenticated.value = false
    cookies.remove("csrftoken")
    cookies.remove("token")
  }

  return { user, isAuthenticated, isLoading, error, login, logout, clearAuth }
})
