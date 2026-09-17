import { z } from "zod"

export const FERTILIZER_TYPES = ["SWAMP", "COMPOST", "OTHER"] as const
export const FERTILIZER_STATUSES = ["BREWING", "READY", "USED", "DISCARDED"] as const

export const fertilizerSchema = z.object({
  name: z.string().min(1, "Name is required"),
  type: z.enum(FERTILIZER_TYPES).default("SWAMP"),
  status: z.enum(FERTILIZER_STATUSES).default("BREWING"),
  startDate: z.string().date(),
  ingredients: z.array(z.string()).default([]),
  notes: z.string().optional(),
})

export type fertilizerForm = z.infer<typeof fertilizerSchema>
