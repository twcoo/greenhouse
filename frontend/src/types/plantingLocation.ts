import type { PlantingLocationStatus } from "./plantingLocationStatus"

export interface PlantingLocation {
  id: number
  name: string
  locationType: string
  height?: number
  width: number
  length?: number
  currentStatus?: PlantingLocationStatus | null
}

export interface PlantingLocationPayload {
  name: string
  locationType: string
  height?: number
  width: number
  length?: number
}
