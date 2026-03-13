import { ref } from "vue"
import { createAdmin } from "@/api/services/setupService"
import type { createAdminPayload, createAdminResponse } from "@/types/setup"
import type { APIErrorResponse } from "@/types/api"
import type { AxiosError } from "axios"

export function useSetup() {
  const loading = ref(false)

  const setupAdmin = async (payload: createAdminPayload): Promise<createAdminResponse | void> => {
    loading.value = true

    try {
      const data = await createAdmin(payload)

      return data
    } catch (err) {
      throw err as AxiosError<APIErrorResponse>
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    setupAdmin,
  }
}
