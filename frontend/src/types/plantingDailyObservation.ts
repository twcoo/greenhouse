export type HealthStatus = "GOOD" | "FAIR" | "POOR"
export type PestPressure = "NONE" | "LOW" | "MEDIUM" | "HIGH"

export interface PlantingDailyObservation {
  id: number
  stage: number | null
  stageName: string | null
  heightCm: string | null
  leafCount: number | null
  temperatureC: string | null
  humidityPercent: string | null
  lightHours: string | null
  soilMoisturePercent: string | null
  soilPh: string | null
  ecMsCm: string | null
  healthStatus: HealthStatus
  pestPressure: PestPressure
  diseaseSymptoms: boolean
  watered: boolean
  notes: string
  image: string | null
  createdAt: string
  updatedAt: string
}

export interface PlantingDailyObservationPayload {
  heightCm?: number
  leafCount?: number
  temperatureC?: number
  humidityPercent?: number
  lightHours?: number
  soilMoisturePercent?: number
  soilPh?: number
  ecMsCm?: number
  healthStatus: HealthStatus
  pestPressure: PestPressure
  diseaseSymptoms: boolean
  watered: boolean
  notes?: string
  image?: File | null
}
