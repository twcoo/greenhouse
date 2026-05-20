import { apiClient } from "@/api/client"
import type { APIResponse, PaginatedAPIResponse, PaginatedResponse } from "@/types/api"
import type {
  PlantingLocationAssignment,
  PlantingLocationAssignmentPayload,
} from "@/types/plantingLocationAssignment"

export const plantingLocationAssignmentService = {
  async getAll(
    plantingId: number,
    page: number = 1,
    pageSize: number = 10,
  ): Promise<PaginatedResponse<PlantingLocationAssignment>> {
    const response = await apiClient.get<PaginatedAPIResponse<PlantingLocationAssignment>>(
      `/plantings/${plantingId}/locations/`,
      {
        params: { page, page_size: pageSize },
      },
    )
    return response.data.data
  },

  async create(plantingId: number, payload: PlantingLocationAssignmentPayload): Promise<void> {
    await apiClient.post<APIResponse<PlantingLocationAssignment>>(
      `/plantings/${plantingId}/locations/`,
      payload,
    )
  },

  async update(
    plantingId: number,
    id: number,
    payload: PlantingLocationAssignmentPayload,
  ): Promise<void> {
    await apiClient.put<APIResponse<PlantingLocationAssignment>>(
      `/plantings/${plantingId}/locations/${id}`,
      payload,
    )
  },

  async delete(plantingId: number, id: number): Promise<void> {
    await apiClient.delete<APIResponse<PlantingLocationAssignment>>(
      `/plantings/${plantingId}/locations/${id}`,
    )
  },
}
