import { computed, type Ref } from "vue"
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query"
import { cropService } from "@/api/services/cropsService"
import type { cropPayload } from "@/types/crop"
import type { APIErrorResponse } from "@/types/api"
import type { AxiosError } from "axios"

export function useCrop(pagination?: Ref<{ pageIndex: number; pageSize: number }>) {
  const queryClient = useQueryClient()

  const {
    data: crops,
    isLoading: isQueryLoading,
    isFetching,
    isError: isQueryError,
    refetch,
  } = useQuery({
    queryKey: ["crops", pagination],
    queryFn: () => {
      const page = pagination?.value ? pagination.value.pageIndex + 1 : 1
      const size = pagination?.value ? pagination.value.pageSize : 10
      return cropService.getAll(page, size)
    },
  })

  const createMutation = useMutation({
    mutationFn: (payload: cropPayload): Promise<void> => cropService.create(payload),
    onSuccess: (): void => {
      queryClient.invalidateQueries({ queryKey: ["crops"] })
    },
    onError: (err: AxiosError<APIErrorResponse>) => {
      throw err
    },
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: cropPayload }): Promise<void> =>
      cropService.update(id, payload),
    onSuccess: (): void => {
      queryClient.invalidateQueries({ queryKey: ["crops"] })
    },
    onError: (err: AxiosError<APIErrorResponse>) => {
      throw err
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id: number): Promise<void> => cropService.delete(id),
    onSuccess: (): void => {
      queryClient.invalidateQueries({ queryKey: ["crops"] })
    },
    onError: (err: AxiosError<APIErrorResponse>) => {
      throw err
    },
  })

  const loading = computed(
    (): boolean =>
      isQueryLoading.value ||
      isFetching.value ||
      createMutation.isPending.value ||
      updateMutation.isPending.value ||
      deleteMutation.isPending.value,
  )

  return {
    // Data
    crops,

    // Status States
    isLoading: loading,
    isQueryError,
    createError: createMutation.isError,
    updateError: updateMutation.isError,
    deleteError: deleteMutation.isError,

    // Success States
    isCreateSuccess: createMutation.isSuccess,
    isUpdateSuccess: updateMutation.isSuccess,
    isDeleteSuccess: deleteMutation.isSuccess,

    // Actions
    createCrop: createMutation.mutateAsync,
    updateCrop: updateMutation.mutateAsync,
    deleteCrop: deleteMutation.mutateAsync,
    fetchCrops: refetch,
  }
}
