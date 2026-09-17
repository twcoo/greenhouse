import { computed, type Ref } from "vue"
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query"
import { fertilizerLogService } from "@/api/services/fertilizerLogService"
import type { FertilizerLogPayload } from "@/types/fertilizerLog"
import type { APIErrorResponse } from "@/types/api"
import type { AxiosError } from "axios"

export function useFertilizerLogs(
  fertilizerId: Ref<number>,
  pagination?: Ref<{ pageIndex: number; pageSize: number }>,
) {
  const queryClient = useQueryClient()

  const {
    data: logs,
    isLoading: isQueryLoading,
    isFetching,
    isError: isQueryError,
    refetch,
  } = useQuery({
    queryKey: ["fertilizer-logs", fertilizerId, pagination],
    queryFn: () => {
      const page = pagination?.value ? pagination.value.pageIndex + 1 : 1
      const size = pagination?.value ? pagination.value.pageSize : 10
      return fertilizerLogService.getAll(fertilizerId.value, page, size)
    },
    enabled: computed(() => fertilizerId.value > 0),
  })

  const createMutation = useMutation({
    mutationFn: (payload: FertilizerLogPayload) =>
      fertilizerLogService.create(fertilizerId.value, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["fertilizer-logs", fertilizerId],
      })
      queryClient.invalidateQueries({
        queryKey: ["fertilizers"],
      })
    },
    onError: (err: AxiosError<APIErrorResponse>) => {
      throw err
    },
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: FertilizerLogPayload }) =>
      fertilizerLogService.update(fertilizerId.value, id, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["fertilizer-logs", fertilizerId],
      })
      queryClient.invalidateQueries({
        queryKey: ["fertilizers"],
      })
    },
    onError: (err: AxiosError<APIErrorResponse>) => {
      throw err
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id: number) => fertilizerLogService.delete(fertilizerId.value, id),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["fertilizer-logs", fertilizerId],
      })
      queryClient.invalidateQueries({
        queryKey: ["fertilizers"],
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
    logs,

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
    createLog: createMutation.mutateAsync,
    updateLog: updateMutation.mutateAsync,
    deleteLog: deleteMutation.mutateAsync,
    fetchLogs: refetch,
  }
}
