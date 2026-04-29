export type PlantingLocationStatusChoice =
  | "AVAILABLE"
  | "IN_USE"
  | "DAMAGED"
  | "DESTROYED"
  | "RETIRED"

export interface PlantingLocationStatus {
  id: number
  status: PlantingLocationStatusChoice
  notes: string
  image?: string | null
  createdAt: string
}

export interface PlantingLocationStatusPayload {
  status: PlantingLocationStatusChoice
  notes?: string
  image?: File
}
