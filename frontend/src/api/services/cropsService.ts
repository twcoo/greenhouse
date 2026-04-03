import { apiClient } from "@/api/client"
import type { APIResponse, PaginatedAPIResponse } from "@/types/api"
import type { Crop, cropPayload } from "@/types/crop"

export const cropService = {
  async getAll(page: number = 1, pageSize: number = 10): Promise<PaginatedAPIResponse<Crop>> {
    const response = await apiClient.get<PaginatedAPIResponse<Crop>>(
      `/crops/?page=${page}&page_size=${pageSize}`,
    )

    return response.data.data
  },

  async create(payload: cropPayload): Promise<Crop> {
    const response = await apiClient.post<APIResponse<Crop>>("/crops/", payload)
    return response.data.data
  },
}
