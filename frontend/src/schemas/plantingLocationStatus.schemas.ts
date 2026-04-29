import { z } from "zod"

export const MANUAL_STATUS_CHOICES = ["DAMAGED", "DESTROYED", "RETIRED"] as const

export const plantingLocationStatusSchema = z.object({
  status: z.enum(MANUAL_STATUS_CHOICES, { error: "Status is required" }),
  notes: z.string().optional(),
  image: z.instanceof(File).optional(),
})

export type PlantingLocationStatusForm = z.infer<typeof plantingLocationStatusSchema>
