import axios from "axios"
import Cookies from "js-cookie"
import { decamelizeKeys, camelizeKeys } from "humps"

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
})

apiClient.interceptors.request.use((config) => {
  if (config.data) {
    config.data = decamelizeKeys(config.data)
  }

  const token = Cookies.get("csrftoken")

  if (token) {
    config.headers["X-CSRFToken"] = token
  }

  return config
})

apiClient.interceptors.response.use((response) => {
  if (response.data) {
    response.data = camelizeKeys(response.data)
  }

  return response
})
