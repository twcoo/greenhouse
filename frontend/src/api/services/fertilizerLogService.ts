import { apiClient } from "@/api/client"
import type { APIResponse, PaginatedAPIResponse, PaginatedResponse } from "@/types/api"
import type { FertilizerLog, FertilizerLogPayload } from "@/types/fertilizerLog"

export const fertilizerLogService = {
  async getAll(
    fertilizerId: number,
    page: number = 1,
    pageSize: number = 10,
  ): Promise<PaginatedResponse<FertilizerLog>> {
    const response = await apiClient.get<PaginatedAPIResponse<FertilizerLog>>(
      `/fertilizers/${fertilizerId}/logs/`,
      { params: { page, page_size: pageSize } },
    )
    return response.data.data
  },

  async create(fertilizerId: number, payload: FertilizerLogPayload): Promise<FertilizerLog> {
    const response = await apiClient.post<APIResponse<FertilizerLog>>(
      `/fertilizers/${fertilizerId}/logs/`,
      payload,
    )
    return response.data.data
  },

  async update(
    fertilizerId: number,
    id: number,
    payload: FertilizerLogPayload,
  ): Promise<FertilizerLog> {
    const response = await apiClient.put<APIResponse<FertilizerLog>>(
      `/fertilizers/${fertilizerId}/logs/${id}`,
      payload,
    )
    return response.data.data
  },

  async delete(fertilizerId: number, id: number): Promise<void> {
    await apiClient.delete<APIResponse<null>>(`/fertilizers/${fertilizerId}/logs/${id}`)
  },
}
