import { z } from "zod"

export const plantingSchema = z.object({
  crop: z.coerce.number().min(1, "Crop is required"),
  variety: z.coerce.number().min(1, "Variety is required"),
})

export type plantingForm = z.infer<typeof plantingSchema>
