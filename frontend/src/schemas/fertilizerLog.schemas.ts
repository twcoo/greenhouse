import { z } from "zod"

export const FERTILIZER_LOG_EVENT_TYPES = [
  "ADDED_INGREDIENT",
  "ADDED_WATER",
  "STIRRED",
  "OTHER",
] as const

export const fertilizerLogSchema = z.object({
  logDate: z.string().date(),
  eventType: z.enum(FERTILIZER_LOG_EVENT_TYPES).default("OTHER"),
  itemAdded: z.string().optional(),
  quantity: z.string().optional(),
  notes: z.string().optional(),
})

export type FertilizerLogForm = z.infer<typeof fertilizerLogSchema>
