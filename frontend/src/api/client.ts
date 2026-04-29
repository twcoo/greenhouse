import axios from "axios"
import Cookies from "js-cookie"
import router from "@/router"
import { decamelizeKeys, camelizeKeys } from "humps"
import { useAuthStore } from "@/stores/authStore"

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
})

apiClient.interceptors.request.use((config) => {
  if (config.data && !(config.data instanceof FormData)) {
    config.data = decamelizeKeys(config.data)
  }

  const csrfToken = Cookies.get("csrftoken")

  if (csrfToken) {
    config.headers["X-CSRFToken"] = csrfToken
  }

  return config
})

apiClient.interceptors.response.use(
  (response) => {
    if (response.data) {
      response.data = camelizeKeys(response.data)
    }

    return response
  },
  (error) => {
    if (error.response?.data) {
      error.response.data = camelizeKeys(error.response.data)
    }

    const status = error.response?.status
    const isLoginPage = router.currentRoute.value.name === "login"

    if ([401, 403].includes(status) && !isLoginPage) {
      const authStore = useAuthStore()

      authStore.clearAuth()
      authStore.error = "Your session has expired. Please login again."

      const redirectTo = router.currentRoute.value.name
      router.push({ name: "login", query: { redirectTo: redirectTo as string } })
    }

    return Promise.reject(error)
  },
)
