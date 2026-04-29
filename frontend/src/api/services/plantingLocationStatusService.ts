import { apiClient } from "@/api/client"
import type { APIResponse, PaginatedAPIResponse, PaginatedResponse } from "@/types/api"
import type {
  PlantingLocationStatus,
  PlantingLocationStatusPayload,
} from "@/types/plantingLocationStatus"

export const plantingLocationStatusService = {
  async getAll(locationId: number): Promise<PaginatedResponse<PlantingLocationStatus>> {
    const response = await apiClient.get<PaginatedAPIResponse<PlantingLocationStatus>>(
      `/planting-locations/${locationId}/statuses/`,
      { params: { page_size: 100 } },
    )
    return response.data.data
  },

  async create(locationId: number, payload: PlantingLocationStatusPayload): Promise<void> {
    const formData = new FormData()
    formData.append("status", payload.status)
    if (payload.notes) formData.append("notes", payload.notes)
    if (payload.image) formData.append("image", payload.image)

    await apiClient.post<APIResponse<PlantingLocationStatus>>(
      `/planting-locations/${locationId}/statuses/`,
      formData,
      { headers: { "Content-Type": "multipart/form-data" } },
    )
  },
}
