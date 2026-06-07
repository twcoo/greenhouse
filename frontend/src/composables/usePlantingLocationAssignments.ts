import { computed, type Ref } from "vue"
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query"
import { plantingLocationAssignmentService } from "@/api/services/plantingLocationAssignmentService"
import type { PlantingLocationAssignmentPayload } from "@/types/plantingLocationAssignment"
import type { APIErrorResponse } from "@/types/api"
import type { AxiosError } from "axios"

export function usePlantingLocationAssignments(
  plantingId: Ref<number>,
  pagination?: Ref<{ pageIndex: number; pageSize: number }>,
) {
  const queryClient = useQueryClient()

  const {
    data: assignments,
    isLoading: isQueryLoading,
    isFetching,
    isError: isQueryError,
    refetch,
  } = useQuery({
    queryKey: ["planting-location-assignments", plantingId, pagination],
    queryFn: () => {
      const page = pagination?.value ? pagination.value.pageIndex + 1 : 1
      const size = pagination?.value ? pagination.value.pageSize : 10
      return plantingLocationAssignmentService.getAll(plantingId.value, page, size)
    },
    enabled: computed(() => plantingId.value > 0),
  })

  const createMutation = useMutation({
    mutationFn: (payload: PlantingLocationAssignmentPayload): Promise<void> =>
      plantingLocationAssignmentService.create(plantingId.value, payload),
    onSuccess: (): void => {
      queryClient.invalidateQueries({ queryKey: ["planting-location-assignments", plantingId] })
      queryClient.invalidateQueries({ queryKey: ["plantings"] })
    },
    onError: (err: AxiosError<APIErrorResponse>) => {
      throw err
    },
  })

  const updateMutation = useMutation({
    mutationFn: ({
      id,
      payload,
    }: {
      id: number
      payload: PlantingLocationAssignmentPayload
    }): Promise<void> => plantingLocationAssignmentService.update(plantingId.value, id, payload),
    onSuccess: (): void => {
      queryClient.invalidateQueries({ queryKey: ["planting-location-assignments", plantingId] })
      queryClient.invalidateQueries({ queryKey: ["plantings"] })
    },
    onError: (err: AxiosError<APIErrorResponse>) => {
      throw err
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id: number): Promise<void> =>
      plantingLocationAssignmentService.delete(plantingId.value, id),
    onSuccess: (): void => {
      queryClient.invalidateQueries({ queryKey: ["planting-location-assignments", plantingId] })
      queryClient.invalidateQueries({ queryKey: ["plantings"] })
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
    assignments,

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
    createAssignment: createMutation.mutateAsync,
    updateAssignment: updateMutation.mutateAsync,
    deleteAssignment: deleteMutation.mutateAsync,
    fetchAssignments: refetch,
  }
}
