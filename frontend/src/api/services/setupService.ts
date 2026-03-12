import { apiClient } from "@/api/client"
import type { APIResponse } from "@/types/api"

export const status = async (): Promise<void> => {
  await apiClient.get<APIResponse<null>>("/setup/status")
}
