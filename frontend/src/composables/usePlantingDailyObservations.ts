import { computed, type Ref } from "vue"
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query"
import { plantingDailyObservationService } from "@/api/services/plantingDailyObservationService"
import type { PlantingDailyObservationPayload } from "@/types/plantingDailyObservation"
import type { APIErrorResponse } from "@/types/api"
import type { AxiosError } from "axios"

export function usePlantingDailyObservations(plantingId: Ref<number>) {
  const queryClient = useQueryClient()

  const {
    data: observations,
    isLoading: isQueryLoading,
    isFetching,
    isError: isQueryError,
    refetch,
  } = useQuery({
    queryKey: ["planting-daily-observations", plantingId],
    queryFn: () => plantingDailyObservationService.getAll(plantingId.value),
    enabled: computed(() => plantingId.value > 0),
  })

  const createMutation = useMutation({
    mutationFn: (payload: PlantingDailyObservationPayload) =>
      plantingDailyObservationService.create(plantingId.value, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["planting-daily-observations", plantingId],
      })
    },
    onError: (err: AxiosError<APIErrorResponse>) => {
      throw err
    },
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: PlantingDailyObservationPayload }) =>
      plantingDailyObservationService.update(plantingId.value, id, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["planting-daily-observations", plantingId],
      })
    },
    onError: (err: AxiosError<APIErrorResponse>) => {
      throw err
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id: number) => plantingDailyObservationService.delete(plantingId.value, id),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["planting-daily-observations", plantingId],
      })
    },
    onError: (err: AxiosError<APIErrorResponse>) => {
      throw err
    },
  })

  const isLoading = computed(
    (): boolean =>
      isQueryLoading.value ||
      isFetching.value ||
      createMutation.isPending.value ||
      updateMutation.isPending.value ||
      deleteMutation.isPending.value,
  )

  return {
    // Data
    observations,

    // Status States
    isLoading,
    isQueryError,
    createError: createMutation.isError,
    updateError: updateMutation.isError,
    deleteError: deleteMutation.isError,

    // Success States
    isCreateSuccess: createMutation.isSuccess,
    isUpdateSuccess: updateMutation.isSuccess,
    isDeleteSuccess: deleteMutation.isSuccess,

    // Actions
    createObservation: createMutation.mutateAsync,
    updateObservation: updateMutation.mutateAsync,
    deleteObservation: deleteMutation.mutateAsync,
    fetchObservations: refetch,
  }
}
