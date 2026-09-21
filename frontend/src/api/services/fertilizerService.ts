import { apiClient } from "@/api/client"
import type { APIResponse, PaginatedAPIResponse, PaginatedResponse } from "@/types/api"
import type { Fertilizer, FertilizerPayload } from "@/types/fertilizer"

export const fertilizerService = {
  async getAll(
    page: number = 1,
    pageSize: number = 10,
    search: string = "",
  ): Promise<PaginatedResponse<Fertilizer>> {
    const response = await apiClient.get<PaginatedAPIResponse<Fertilizer>>("/fertilizers/", {
      params: {
        page,
        page_size: pageSize,
        search: search || undefined,
      },
    })

    return response.data.data
  },

  async create(payload: FertilizerPayload): Promise<void> {
    await apiClient.post<APIResponse<Fertilizer>>("/fertilizers/", payload)
  },

  async update(id: number, payload: FertilizerPayload): Promise<void> {
    await apiClient.put<APIResponse<Fertilizer>>(`/fertilizers/${id}`, payload)
  },

  async delete(id: number): Promise<void> {
    await apiClient.delete<APIResponse<Fertilizer>>(`/fertilizers/${id}`)
  },
}
