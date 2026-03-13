import { apiClient } from "@/api/client"
import type { APIResponse } from "@/types/api"
import type { createAdminPayload, createAdminResponse } from "@/types/setup"

export const createAdmin = async (payload: createAdminPayload): Promise<createAdminResponse> => {
  const response = await apiClient.post<APIResponse<createAdminResponse>>("setup/admin", payload)

  return response.data.data
}

export const status = async (): Promise<void> => {
  await apiClient.get<APIResponse<null>>("/setup/status")
}
