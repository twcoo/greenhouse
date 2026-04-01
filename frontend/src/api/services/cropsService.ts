import { apiClient } from "@/api/client"
import type { APIResponse, PaginatedAPIResponse } from "@/types/api"
import type { Crop, cropPayload } from "@/types/crop"

export const getCrops = async (): Promise<PaginatedAPIResponse<Crop>> => {
  const response = await apiClient.get<PaginatedAPIResponse<Crop>>("crops/")

  return response.data
}

export const createCrop = async (payload: cropPayload): Promise<Crop> => {
  const response = await apiClient.post<APIResponse<Crop>>("crops/", payload)

  return response.data
}
