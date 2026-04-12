import { apiClient } from "@/api/client"
import type { APIResponse, PaginatedAPIResponse, PaginatedResponse } from "@/types/api"
import type { Crop, cropPayload } from "@/types/crop"

export const cropService = {
  async getAll(
    page: number = 1,
    pageSize: number = 10,
    search: string = "",
  ): Promise<PaginatedResponse<Crop>> {
    const response = await apiClient.get<PaginatedAPIResponse<Crop>>("/crops/", {
      params: {
        page,
        page_size: pageSize,
        search: search || undefined,
      },
    })

    return response.data.data
  },

  async create(payload: cropPayload): Promise<void> {
    await apiClient.post<APIResponse<Crop>>("/crops/", payload)
  },

  async update(id: number, payload: cropPayload): Promise<void> {
    await apiClient.put<APIResponse<Crop>>(`/crops/${id}`, payload)
  },

  async delete(id: number): Promise<void> {
    await apiClient.delete<APIResponse<Crop>>(`/crops/${id}`)
  },
}
