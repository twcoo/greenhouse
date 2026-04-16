import { computed, type Ref } from "vue"
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query"
import { varietyService } from "@/api/services/varietyService"
import type { VarietyPayload } from "@/types/variety"
import type { APIErrorResponse } from "@/types/api"
import type { AxiosError } from "axios"

export function useVarieties(
  pagination?: Ref<{ pageIndex: number; pageSize: number }>,
  searchTerm?: Ref<string>,
) {
  const queryClient = useQueryClient()

  const {
    data: varieties,
    isLoading: isQueryLoading,
    isFetching,
    isError: isQueryError,
    refetch,
  } = useQuery({
    queryKey: ["varieties", pagination, "search"],
    queryFn: () => {
      const page = pagination?.value ? pagination.value.pageIndex + 1 : 1
      const size = pagination?.value ? pagination.value.pageSize : 10
      const search = searchTerm?.value || ""

      return varietyService.getAll(page, size, search)
    },
  })

  const createMutation = useMutation({
    mutationFn: (payload: VarietyPayload): Promise<void> => varietyService.create(payload),
    onSuccess: (): void => {
      queryClient.invalidateQueries({ queryKey: ["varieties"] })
    },
    onError: (err: AxiosError<APIErrorResponse>) => {
      throw err
    },
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: VarietyPayload }): Promise<void> =>
      varietyService.update(id, payload),
    onSuccess: (): void => {
      queryClient.invalidateQueries({ queryKey: ["varieties"] })
    },
    onError: (err: AxiosError<APIErrorResponse>) => {
      throw err
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id: number): Promise<void> => varietyService.delete(id),
    onSuccess: (): void => {
      queryClient.invalidateQueries({ queryKey: ["varieties"] })
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
    varieties,

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
    createVariety: createMutation.mutateAsync,
    updateVariety: updateMutation.mutateAsync,
    deleteVariety: deleteMutation.mutateAsync,
    fetchVarieties: refetch,
  }
}
