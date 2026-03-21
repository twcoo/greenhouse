import { apiClient } from "@/api/client"
import type { APIResponse } from "@/types/api"
import type { authLoginData, authLoginPayload } from "@/types/auth"

export const authLogin = async (payload: authLoginPayload): Promise<authLoginData> => {
  const response = await apiClient.post<APIResponse<authLoginData>>("auth/login", payload)

  return response.data.data
}

export const authLogout = async (): Promise<void> => {
  await apiClient.post<APIResponse<null>>("auth/logout")
}
