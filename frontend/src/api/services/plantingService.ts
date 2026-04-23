import { apiClient } from "@/api/client"
import type { APIResponse, PaginatedAPIResponse, PaginatedResponse } from "@/types/api"
import type { Planting, PlantingPayload } from "@/types/planting"

export const plantingService = {
  async getAll(
    page: number = 1,
    pageSize: number = 10,
    search: string = "",
  ): Promise<PaginatedResponse<Planting>> {
    const response = await apiClient.get<PaginatedAPIResponse<Planting>>("/plantings/", {
      params: {
        page,
        page_size: pageSize,
        search: search || undefined,
      },
    })

    return response.data.data
  },

  async create(payload: PlantingPayload): Promise<void> {
    await apiClient.post<APIResponse<Planting>>("/plantings/", payload)
  },

  async update(id: number, payload: PlantingPayload): Promise<void> {
    await apiClient.put<APIResponse<Planting>>(`/plantings/${id}`, payload)
  },

  async delete(id: number): Promise<void> {
    await apiClient.delete<APIResponse<Planting>>(`/plantings/${id}`)
  },
}
