export type HealthStatus = "GOOD" | "FAIR" | "POOR"
export type PestPressure = "NONE" | "LOW" | "MEDIUM" | "HIGH"
export type FertilizerType = "NONE" | "ORGANIC" | "SYNTHETIC"
export type WateringEvent = "WATERED" | "RAINED" | "SKIPPED_WET"

export interface PlantingDailyObservation {
  id: number
  stage: number | null
  stageName: string | null
  healthStatus: HealthStatus
  pestPressure: PestPressure
  diseaseSymptoms: boolean
  wateringEvent: WateringEvent | null
  fertilizerType: FertilizerType
  fertilizerDetail: string
  pruned: boolean
  pruningDetail: string
  notes: string
  image: string | null
  observationDate: string
  createdAt: string
  updatedAt: string
}

export interface PlantingDailyObservationPayload {
  healthStatus: HealthStatus
  pestPressure: PestPressure
  diseaseSymptoms: boolean
  wateringEvent?: WateringEvent | null
  fertilizerType?: FertilizerType
  fertilizerDetail?: string
  pruned: boolean
  pruningDetail?: string
  notes?: string
  image?: File | null
  observationDate?: string
}
