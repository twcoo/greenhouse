import { z } from "zod"

export const CategoryEnum = z.enum(["VEGETABLE", "FRUIT"])
export const SunlightRequirementEnum = z.enum(["FULL SUN", "PART SUN", "FULL SHADE"])

export const cropsSchema = z
  .object({
    name: z.string().min(1, "Name is required"),
    scientificName: z.string().min(1, "Scientific name is required"),
    category: CategoryEnum,
    sunlightRequirement: SunlightRequirementEnum,
    minDaysToHarvest: z.coerce.number().min(1, "Must be at least 1"),
    maxDaysToHarvest: z.coerce.number().min(1, "Must be at least 1"),
  })
  .refine((data) => data.maxDaysToHarvest >= data.minDaysToHarvest, {
    message: "Max days must be ≥ min days",
    path: ["maxDaysToHarvest"],
  })

export type cropsForm = z.infer<typeof cropsSchema>
