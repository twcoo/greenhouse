export interface Planting {
  id: number
  crop: number
  cropName: string
  variety: number
  varietyName: string
  currentLocation: string | null
  createdAt: string
}

export interface PlantingPayload {
  crop: number
  variety: number
}
