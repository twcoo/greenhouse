export type FertilizerType = "SWAMP" | "COMPOST" | "OTHER"
export type FertilizerStatus = "BREWING" | "READY" | "USED" | "DISCARDED"

export interface Fertilizer {
  id: number
  name: string
  type: FertilizerType
  status: FertilizerStatus
  startDate: string
  ingredients: string[]
  notes: string
  createdAt: string
  updatedAt: string
}

export interface FertilizerPayload {
  name: string
  type?: FertilizerType
  status?: FertilizerStatus
  startDate?: string
  ingredients?: string[]
  notes?: string
}
