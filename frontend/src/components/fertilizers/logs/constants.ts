import type { FertilizerLogEventType } from "@/types/fertilizerLog"

export const EVENT_TYPE_OPTIONS: { value: FertilizerLogEventType; label: string }[] = [
  { value: "ADDED_INGREDIENT", label: "Added Ingredient" },
  { value: "ADDED_WATER", label: "Added Water" },
  { value: "STIRRED", label: "Stirred" },
  { value: "OTHER", label: "Other" },
]

export const EVENT_TYPE_LABEL: Record<FertilizerLogEventType, string> = {
  ADDED_INGREDIENT: "Added Ingredient",
  ADDED_WATER: "Added Water",
  STIRRED: "Stirred",
  OTHER: "Other",
}
