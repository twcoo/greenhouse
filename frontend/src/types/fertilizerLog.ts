export type FertilizerLogEventType = "ADDED_INGREDIENT" | "ADDED_WATER" | "STIRRED" | "OTHER"

export interface FertilizerLog {
  id: number
  eventType: FertilizerLogEventType
  itemAdded: string
  quantity: string
  notes: string
  logDate: string
  createdAt: string
  updatedAt: string
}

export interface FertilizerLogPayload {
  eventType?: FertilizerLogEventType
  itemAdded?: string
  quantity?: string
  notes?: string
  logDate?: string
}
