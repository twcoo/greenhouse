import { z } from "zod"

export const GrowthHabitEnum = z.enum(["DETERMINATE", "INDETERMINATE"])

export const varietySchema = z.object({
  name: z.string().min(1, "Name is required"),
  crop: z.coerce.number().min(1, "Crop is required"),
  growthHabit: z.array(GrowthHabitEnum).min(1, "Growth habit is required"),
})

export type varietyForm = z.infer<typeof varietySchema>
