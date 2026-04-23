import { computed, type Ref } from "vue"
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query"
import { plantingService } from "@/api/services/plantingService"
import type { PlantingPayload } from "@/types/planting"
import type { APIErrorResponse } from "@/types/api"
import type { AxiosError } from "axios"

export function usePlantings(
  pagination?: Ref<{ pageIndex: number; pageSize: number }>,
  searchTerm?: Ref<string>,
) {
  const queryClient = useQueryClient()

  const {
    data: plantings,
    isLoading: isQueryLoading,
    isFetching,
    isError: isQueryError,
    refetch,
  } = useQuery({
    queryKey: ["plantings", pagination, "search"],
    queryFn: () => {
      const page = pagination?.value ? pagination.value.pageIndex + 1 : 1
      const size = pagination?.value ? pagination.value.pageSize : 10
      const search = searchTerm?.value || ""

      return plantingService.getAll(page, size, search)
    },
  })

  const createMutation = useMutation({
    mutationFn: (payload: PlantingPayload): Promise<void> => plantingService.create(payload),
    onSuccess: (): void => {
      queryClient.invalidateQueries({ queryKey: ["plantings"] })
    },
    onError: (err: AxiosError<APIErrorResponse>) => {
      throw err
    },
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: PlantingPayload }): Promise<void> =>
      plantingService.update(id, payload),
    onSuccess: (): void => {
      queryClient.invalidateQueries({ queryKey: ["plantings"] })
    },
    onError: (err: AxiosError<APIErrorResponse>) => {
      throw err
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id: number): Promise<void> => plantingService.delete(id),
    onSuccess: (): void => {
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
    plantings,

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
    createPlanting: createMutation.mutateAsync,
    updatePlanting: updateMutation.mutateAsync,
    deletePlanting: deleteMutation.mutateAsync,
    fetchPlantings: refetch,
  }
}
