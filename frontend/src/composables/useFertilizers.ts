import { computed, type Ref } from "vue"
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query"
import { fertilizerService } from "@/api/services/fertilizerService"
import type { FertilizerPayload } from "@/types/fertilizer"
import type { APIErrorResponse } from "@/types/api"
import type { AxiosError } from "axios"

export function useFertilizers(
  pagination?: Ref<{ pageIndex: number; pageSize: number }>,
  searchTerm?: Ref<string>,
) {
  const queryClient = useQueryClient()

  const {
    data: fertilizers,
    isLoading: isQueryLoading,
    isFetching,
    isError: isQueryError,
    refetch,
  } = useQuery({
    queryKey: ["fertilizers", pagination, "search"],
    queryFn: () => {
      const page = pagination?.value ? pagination.value.pageIndex + 1 : 1
      const size = pagination?.value ? pagination.value.pageSize : 10
      const search = searchTerm?.value || ""

      return fertilizerService.getAll(page, size, search)
    },
  })

  const createMutation = useMutation({
    mutationFn: (payload: FertilizerPayload): Promise<void> => fertilizerService.create(payload),
    onSuccess: (): void => {
      queryClient.invalidateQueries({ queryKey: ["fertilizers"] })
    },
    onError: (err: AxiosError<APIErrorResponse>) => {
      throw err
    },
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: FertilizerPayload }): Promise<void> =>
      fertilizerService.update(id, payload),
    onSuccess: (): void => {
      queryClient.invalidateQueries({ queryKey: ["fertilizers"] })
    },
    onError: (err: AxiosError<APIErrorResponse>) => {
      throw err
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id: number): Promise<void> => fertilizerService.delete(id),
    onSuccess: (): void => {
      queryClient.invalidateQueries({ queryKey: ["fertilizers"] })
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
    fertilizers,

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
    createFertilizer: createMutation.mutateAsync,
    updateFertilizer: updateMutation.mutateAsync,
    deleteFertilizer: deleteMutation.mutateAsync,
    fetchFertilizers: refetch,
  }
}
