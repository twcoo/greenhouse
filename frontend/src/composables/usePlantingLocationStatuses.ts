import { computed, type Ref } from "vue"
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query"
import { plantingLocationStatusService } from "@/api/services/plantingLocationStatusService"
import type { PlantingLocationStatusPayload } from "@/types/plantingLocationStatus"
import type { APIErrorResponse } from "@/types/api"
import type { AxiosError } from "axios"

export function usePlantingLocationStatuses(locationId: Ref<number | null>) {
  const queryClient = useQueryClient()

  const {
    data: statuses,
    isLoading: isQueryLoading,
    isFetching,
    isError: isQueryError,
  } = useQuery({
    queryKey: ["planting-location-statuses", locationId],
    queryFn: () => plantingLocationStatusService.getAll(locationId.value!),
    enabled: computed(() => locationId.value !== null),
  })

  const createMutation = useMutation({
    mutationFn: ({
      id,
      payload,
    }: {
      id: number
      payload: PlantingLocationStatusPayload
    }): Promise<void> => plantingLocationStatusService.create(id, payload),
    onSuccess: (): void => {
      queryClient.invalidateQueries({ queryKey: ["planting-location-statuses", locationId] })
      queryClient.invalidateQueries({ queryKey: ["planting-locations"] })
    },
    onError: (err: AxiosError<APIErrorResponse>) => {
      throw err
    },
  })

  const isLoading = computed(
    (): boolean => isQueryLoading.value || isFetching.value || createMutation.isPending.value,
  )

  return {
    // Data
    statuses,

    // Status States
    isLoading,
    isQueryError,
    createError: createMutation.isError,

    // Success States
    isCreateSuccess: createMutation.isSuccess,

    // Actions
    createStatus: createMutation.mutateAsync,
  }
}
