import { apiClient } from "@/api/client"
import type { APIResponse, PaginatedAPIResponse, PaginatedResponse } from "@/types/api"
import type { PlantingLocation, PlantingLocationPayload } from "@/types/plantingLocation"

export const plantingLocationService = {
  async getAll(
    page: number = 1,
    pageSize: number = 10,
    search: string = "",
  ): Promise<PaginatedResponse<PlantingLocation>> {
    const response = await apiClient.get<PaginatedAPIResponse<PlantingLocation>>(
      "/planting-locations/",
      {
        params: {
          page,
          page_size: pageSize,
          search: search || undefined,
        },
      },
    )

    return response.data.data
  },

  async create(payload: PlantingLocationPayload): Promise<void> {
    await apiClient.post<APIResponse<PlantingLocation>>("/planting-locations/", payload)
  },

  async update(id: number, payload: PlantingLocationPayload): Promise<void> {
    await apiClient.put<APIResponse<PlantingLocation>>(`/planting-locations/${id}`, payload)
  },

  async delete(id: number): Promise<void> {
    await apiClient.delete<APIResponse<PlantingLocation>>(`/planting-locations/${id}`)
  },

  async uploadImage(id: number, file: File): Promise<void> {
    const formData = new FormData()
    formData.append("image", file)
    await apiClient.post(`/planting-locations/${id}/image/`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    })
  },
}
