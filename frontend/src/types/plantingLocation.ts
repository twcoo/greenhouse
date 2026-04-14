export interface PlantingLocation {
  id: number
  name: string
  locationType: string
  height?: number
  width: number
  length?: number
  image?: string
}

export interface PlantingLocationPayload {
  name: string
  locationType: string
  height?: number
  width: number
  length?: number
}
