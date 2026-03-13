import * as z from "zod"

export const setupAdminSchema = z
  .object({
    username: z
      .string()
      .min(3, "Username must be at least 3 characters")
      .max(30, "Username must be less than 30 characters"),
    password: z.string().min(8, "Password must be at least 8 characters"),
    password2: z.string(),
  })
  .refine((data) => data.password === data.password2, {
    path: ["password2"],
    message: "Password do not match",
  })

export type setupAdminForm = z.infer<typeof setupAdminSchema>
