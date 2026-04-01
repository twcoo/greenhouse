export interface Crop {
  id: number
  name: string
  scientificName: string
  category: string
  sunlightRequirement: string
  minDaysToHarvest: number
  maxDaysToHarvest: number
}

export interface cropPayload {
  name: string
  scientificName: string
  category: string
  sunlightRequirement: string
  minDaysToHarvest: number
  maxDaysToHarvest: number
}
