import type { HealthStatus, PestPressure } from "@/types/plantingDailyObservation"

export const HEALTH_STATUS_OPTIONS: { value: HealthStatus; label: string }[] = [
  { value: "GOOD", label: "Good" },
  { value: "FAIR", label: "Fair" },
  { value: "POOR", label: "Poor" },
]

export const PEST_PRESSURE_OPTIONS: { value: PestPressure; label: string }[] = [
  { value: "NONE", label: "None" },
  { value: "LOW", label: "Low" },
  { value: "MEDIUM", label: "Medium" },
  { value: "HIGH", label: "High" },
]

export const HEALTH_BADGE_VARIANT: Record<
  HealthStatus,
  "secondary" | "default" | "destructive" | "outline"
> = {
  GOOD: "secondary",
  FAIR: "outline",
  POOR: "destructive",
}

export const HEALTH_LABEL: Record<HealthStatus, string> = {
  GOOD: "Good",
  FAIR: "Fair",
  POOR: "Poor",
}

export const PEST_PRESSURE_LABEL: Record<PestPressure, string> = {
  NONE: "None",
  LOW: "Low",
  MEDIUM: "Medium",
  HIGH: "High",
}
