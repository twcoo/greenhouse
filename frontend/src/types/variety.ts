export interface Variety {
  id: number
  name: string
  crop: number
  growthHabit: string[]
}

export interface VarietyPayload {
  name: string
  crop: number
  growthHabit: string[]
}
