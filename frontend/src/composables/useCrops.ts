import { computed, type Ref } from "vue"
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query"
import { cropService } from "@/api/services/cropsService"
import type { Crop, cropPayload } from "@/types/crop"
import type { APIErrorResponse } from "@/types/api"
import type { AxiosError } from "axios"

export function useCrop(pagination?: Ref<{ pageIndex: number; pageSize: number }>) {
  const queryClient = useQueryClient()

  const {
    data: crops,
    isLoading,
    isFetching,
    isError,
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
    mutationFn: (payload: cropPayload): Promise<Crop> => cropService.create(payload),
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
    (): boolean => isLoading.value || isFetching.value || createMutation.isPending.value,
  )

  return {
    crops,
    isLoading: loading,
    isError,
    createError: createMutation.isError,
    createCrop: createMutation.mutateAsync,
    deleteCrop: deleteMutation.mutateAsync,
    fetchCrops: refetch,
  }
}
