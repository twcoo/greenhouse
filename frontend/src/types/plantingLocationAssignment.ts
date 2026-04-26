export interface PlantingLocationAssignment {
  id: number
  plantingLocation: number
  plantingLocationName: string
  startDate: string
  endDate: string | null
  createdAt: string
  updatedAt: string
}

export interface PlantingLocationAssignmentPayload {
  plantingLocation: number
  startDate: string
  endDate?: string
}
