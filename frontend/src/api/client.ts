import axios from "axios"
import Cookies from "js-cookie"

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
})

apiClient.interceptors.request.use((config) => {
  const token = Cookies.get("csrftoken")

  if (token) {
    config.headers["X-CSRFToken"] = token
  }

  return config
})
