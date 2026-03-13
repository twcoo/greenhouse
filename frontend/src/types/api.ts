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
