import { z } from "zod"

export const plantingDailyObservationSchema = z.object({
  observationDate: z.string().date(),
  healthStatus: z.enum(["GOOD", "FAIR", "POOR"], {
    error: "Health status is required",
  }),
  pestPressure: z.enum(["NONE", "LOW", "MEDIUM", "HIGH"], {
    error: "Pest pressure is required",
  }),
  diseaseSymptoms: z.boolean(),
  wateringEvent: z.enum(["WATERED", "RAINED", "SKIPPED_WET"]).nullable().optional(),
  fertilizerType: z.enum(["NONE", "ORGANIC", "SYNTHETIC"]).default("NONE"),
  fertilizerDetail: z.string().optional(),
  pruned: z.preprocess((v) => v ?? false, z.boolean()),
  pruningDetail: z.string().optional(),
  notes: z.string().optional(),
  image: z.instanceof(File).nullable().optional(),
})

export type PlantingDailyObservationForm = z.infer<typeof plantingDailyObservationSchema>
