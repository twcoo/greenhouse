import { apiClient } from "@/api/client"
import type { APIResponse, PaginatedAPIResponse, PaginatedResponse } from "@/types/api"
import type { Variety, VarietyPayload } from "@/types/variety"

export const varietyService = {
  async getAll(
    page: number = 1,
    pageSize: number = 10,
    search: string = "",
  ): Promise<PaginatedResponse<Variety>> {
    const response = await apiClient.get<PaginatedAPIResponse<Variety>>("/varieties/", {
      params: {
        page,
        page_size: pageSize,
        search: search || undefined,
      },
    })

    return response.data.data
  },

  async create(payload: VarietyPayload): Promise<void> {
    await apiClient.post<APIResponse<Variety>>("/varieties/", payload)
  },

  async update(id: number, payload: VarietyPayload): Promise<void> {
    await apiClient.put<APIResponse<Variety>>(`/varieties/${id}`, payload)
  },

  async delete(id: number): Promise<void> {
    await apiClient.delete<APIResponse<Variety>>(`/varieties/${id}`)
  },
}
