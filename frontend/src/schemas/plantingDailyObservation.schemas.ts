import { z } from "zod"

const optionalDecimal = () =>
  z.preprocess((v) => (v === "" ? undefined : v), z.coerce.number().optional())

export const plantingDailyObservationSchema = z.object({
  healthStatus: z.enum(["GOOD", "FAIR", "POOR"], {
    error: "Health status is required",
  }),
  pestPressure: z.enum(["NONE", "LOW", "MEDIUM", "HIGH"], {
    error: "Pest pressure is required",
  }),
  diseaseSymptoms: z.boolean(),
  heightCm: optionalDecimal(),
  leafCount: z.preprocess(
    (v) => (v === "" ? undefined : v),
    z.coerce.number().int().nonnegative().optional(),
  ),
  temperatureC: optionalDecimal(),
  humidityPercent: optionalDecimal(),
  lightHours: optionalDecimal(),
  soilMoisturePercent: optionalDecimal(),
  soilPh: optionalDecimal(),
  ecMsCm: optionalDecimal(),
  notes: z.string().optional(),
  image: z.instanceof(File).optional(),
})

export type PlantingDailyObservationForm = z.infer<typeof plantingDailyObservationSchema>
