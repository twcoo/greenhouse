import { z } from "zod"

export const PLANTING_STATUSES = ["ACTIVE", "HARVESTED", "DEAD", "REMOVED"] as const

export const plantingSchema = z.object({
  crop: z.coerce.number().min(1, "Crop is required"),
  variety: z.coerce.number().min(1, "Variety is required"),
  status: z.enum(PLANTING_STATUSES).optional(),
})

export type plantingForm = z.infer<typeof plantingSchema>
