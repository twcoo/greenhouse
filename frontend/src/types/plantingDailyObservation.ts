export type HealthStatus = "GOOD" | "FAIR" | "POOR"
export type PestPressure = "NONE" | "LOW" | "MEDIUM" | "HIGH"
export type FertilizerType = "NONE" | "ORGANIC" | "SYNTHETIC"

export interface PlantingDailyObservation {
  id: number
  stage: number | null
  stageName: string | null
  healthStatus: HealthStatus
  pestPressure: PestPressure
  diseaseSymptoms: boolean
  watered: boolean
  rained: boolean
  fertilizerType: FertilizerType
  fertilizerDetail: string
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
  watered: boolean
  rained: boolean
  fertilizerType?: FertilizerType
  fertilizerDetail?: string
  notes?: string
  image?: File | null
  observationDate?: string
}
