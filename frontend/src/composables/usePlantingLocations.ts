import { computed, type Ref } from "vue"
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query"
import { plantingLocationService } from "@/api/services/plantingLocationService"
import type { PlantingLocationPayload } from "@/types/plantingLocation"
import type { APIErrorResponse } from "@/types/api"
import type { AxiosError } from "axios"

export function usePlantingLocations(
  pagination?: Ref<{ pageIndex: number; pageSize: number }>,
  searchTerm?: Ref<string>,
) {
  const queryClient = useQueryClient()

  const {
    data: locations,
    isLoading: isQueryLoading,
    isFetching,
    isError: isQueryError,
    refetch,
  } = useQuery({
    queryKey: ["planting-locations", pagination, "search"],
    queryFn: () => {
      const page = pagination?.value ? pagination.value.pageIndex + 1 : 1
      const size = pagination?.value ? pagination.value.pageSize : 10
      const search = searchTerm?.value || ""

      return plantingLocationService.getAll(page, size, search)
    },
  })

  const createMutation = useMutation({
    mutationFn: (payload: PlantingLocationPayload): Promise<void> =>
      plantingLocationService.create(payload),
    onSuccess: (): void => {
      queryClient.invalidateQueries({ queryKey: ["planting-locations"] })
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
      payload: PlantingLocationPayload
    }): Promise<void> => plantingLocationService.update(id, payload),
    onSuccess: (): void => {
      queryClient.invalidateQueries({ queryKey: ["planting-locations"] })
    },
    onError: (err: AxiosError<APIErrorResponse>) => {
      throw err
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id: number): Promise<void> => plantingLocationService.delete(id),
    onSuccess: (): void => {
      queryClient.invalidateQueries({ queryKey: ["planting-locations"] })
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
    locations,

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
    createLocation: createMutation.mutateAsync,
    updateLocation: updateMutation.mutateAsync,
    deleteLocation: deleteMutation.mutateAsync,
    fetchLocations: refetch,
  }
}
