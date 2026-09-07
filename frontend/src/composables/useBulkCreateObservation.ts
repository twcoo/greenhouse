import { useMutation, useQueryClient } from "@tanstack/vue-query"
import { plantingDailyObservationService } from "@/api/services/plantingDailyObservationService"
import type { PlantingDailyObservationPayload } from "@/types/plantingDailyObservation"
import type { APIErrorResponse } from "@/types/api"
import type { AxiosError } from "axios"

export function useBulkCreateObservation() {
  const queryClient = useQueryClient()

  const bulkCreateMutation = useMutation({
    mutationFn: ({
      plantingIds,
      payload,
    }: {
      plantingIds: number[]
      payload: PlantingDailyObservationPayload
    }) => plantingDailyObservationService.bulkCreate(plantingIds, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["plantings"] })
    },
    onError: (err: AxiosError<APIErrorResponse>) => {
      throw err
    },
  })

  return {
    bulkCreate: bulkCreateMutation.mutateAsync,
    isPending: bulkCreateMutation.isPending,
    isSuccess: bulkCreateMutation.isSuccess,
  }
}
