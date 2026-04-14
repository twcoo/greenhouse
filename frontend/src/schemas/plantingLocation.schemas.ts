import { z } from "zod"

export const LocationTypeEnum = z.enum(["NURSERYPOT", "POT", "GROUND"])

export const plantingLocationSchema = z
  .object({
    name: z.string().min(1, "Name is required"),
    locationType: LocationTypeEnum,
    height: z.coerce.number().optional(),
    width: z.coerce.number().min(0.1, "Width is required"),
    length: z.coerce.number().optional(),
  })
  .refine(
    (data) => {
      if (data.locationType === "GROUND" && !data.length) {
        return false
      }
      return true
    },
    {
      message: "Length is required for ground locations",
      path: ["length"],
    },
  )
  .refine(
    (data) => {
      if (["NURSERYPOT", "POT"].includes(data.locationType) && !data.height) {
        return false
      }
      return true
    },
    {
      message: "Height is required for pot locations",
      path: ["height"],
    },
  )

export type PlantingLocationForm = z.infer<typeof plantingLocationSchema>
