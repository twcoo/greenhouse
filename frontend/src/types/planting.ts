export type PlantingStatus = "ACTIVE" | "HARVESTED" | "DEAD" | "REMOVED"

export interface Planting {
  id: number
  crop: number
  cropName: string
  variety: number
  varietyName: string
  status: PlantingStatus
  currentLocation: string | null
  hasDailyObservation: boolean
  createdAt: string
}

export interface PlantingPayload {
  crop: number
  variety: number
  status?: PlantingStatus
}
