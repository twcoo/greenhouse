import { apiClient } from "@/api/client"
import { toFormData } from "@/utils/formData"
import type { APIResponse, PaginatedAPIResponse, PaginatedResponse } from "@/types/api"
import type {
  PlantingLocationStatus,
  PlantingLocationStatusPayload,
} from "@/types/plantingLocationStatus"

export const plantingLocationStatusService = {
  async getAll(
    locationId: number,
    page: number = 1,
    pageSize: number = 10,
  ): Promise<PaginatedResponse<PlantingLocationStatus>> {
    const response = await apiClient.get<PaginatedAPIResponse<PlantingLocationStatus>>(
      `/planting-locations/${locationId}/statuses/`,
      { params: { page, page_size: pageSize } },
    )
    return response.data.data
  },

  async create(locationId: number, payload: PlantingLocationStatusPayload): Promise<void> {
    await apiClient.post<APIResponse<PlantingLocationStatus>>(
      `/planting-locations/${locationId}/statuses/`,
      toFormData(payload),
      { headers: { "Content-Type": "multipart/form-data" } },
    )
  },
}
