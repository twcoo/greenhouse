import { z } from "zod"

export const plantingLocationAssignmentSchema = z
  .object({
    plantingLocation: z.coerce.number().min(1, "Location is required"),
    startDate: z.string().min(1, "Start date is required"),
    endDate: z.string().optional(),
  })
  .refine(
    (data) => {
      if (data.endDate && data.startDate) {
        return data.endDate >= data.startDate
      }
      return true
    },
    {
      message: "End date must be on or after start date",
      path: ["endDate"],
    },
  )

export type PlantingLocationAssignmentForm = z.infer<typeof plantingLocationAssignmentSchema>
