export interface APIResponse<T> {
  status: string
  data: T
  message: string
}

export interface APIErrorResponse {
  status: "error"
  data: null
  message: Record<string, string[]> | string
}

export type PaginatedResponse<T> = {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export type PaginatedAPIResponse<T> = APIResponse<PaginatedResponse<T>>
