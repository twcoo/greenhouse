import { ref } from "vue"
import { createCrop as createCropRequest } from "@/api/services/cropsService"
import type { Crop, cropPayload } from "@/types/crop"
import type { APIErrorResponse } from "@/types/api"
import type { AxiosError } from "axios"

export function useCrop() {
  const loading = ref(false)

  const createCrop = async (payload: cropPayload): Promise<Crop | void> => {
    loading.value = true

    try {
      const data = await createCropRequest(payload)

      return data
    } catch (err) {
      throw err as AxiosError<APIErrorResponse>
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    createCrop,
  }
}
