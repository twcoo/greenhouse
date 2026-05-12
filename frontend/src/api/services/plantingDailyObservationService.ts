import { apiClient } from "@/api/client"
import { toFormData } from "@/utils/formData"
import type { APIResponse, PaginatedAPIResponse, PaginatedResponse } from "@/types/api"
import type {
  PlantingDailyObservation,
  PlantingDailyObservationPayload,
} from "@/types/plantingDailyObservation"

export const plantingDailyObservationService = {
  async getAll(
    plantingId: number,
    page: number = 1,
    pageSize: number = 10,
  ): Promise<PaginatedResponse<PlantingDailyObservation>> {
    const response = await apiClient.get<PaginatedAPIResponse<PlantingDailyObservation>>(
      `/plantings/${plantingId}/observations/`,
      { params: { page, page_size: pageSize } },
    )
    return response.data.data
  },

  async create(
    plantingId: number,
    payload: PlantingDailyObservationPayload,
  ): Promise<PlantingDailyObservation> {
    const response = await apiClient.post<APIResponse<PlantingDailyObservation>>(
      `/plantings/${plantingId}/observations/`,
      toFormData(payload),
      { headers: { "Content-Type": "multipart/form-data" } },
    )
    return response.data.data
  },

  async update(
    plantingId: number,
    id: number,
    payload: PlantingDailyObservationPayload,
  ): Promise<PlantingDailyObservation> {
    const response = await apiClient.put<APIResponse<PlantingDailyObservation>>(
      `/plantings/${plantingId}/observations/${id}`,
      toFormData(payload),
      { headers: { "Content-Type": "multipart/form-data" } },
    )
    return response.data.data
  },

  async delete(plantingId: number, id: number): Promise<void> {
    await apiClient.delete<APIResponse<null>>(`/plantings/${plantingId}/observations/${id}`)
  },
}
