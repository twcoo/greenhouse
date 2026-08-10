export type HealthStatus = "GOOD" | "FAIR" | "POOR"
export type PestPressure = "NONE" | "LOW" | "MEDIUM" | "HIGH"

export interface PlantingDailyObservation {
  id: number
  stage: number | null
  stageName: string | null
  healthStatus: HealthStatus
  pestPressure: PestPressure
  diseaseSymptoms: boolean
  watered: boolean
  rained: boolean
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
  notes?: string
  image?: File | null
  observationDate?: string
}
