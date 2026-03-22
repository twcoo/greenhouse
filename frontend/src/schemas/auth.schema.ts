import { z } from "zod"

export const authLoginSchema = z.object({
  username: z.string().min(1, "Username is required"),
  password: z.string().min(1, "Password is required"),
})

export type loginForm = z.infer<typeof authLoginSchema>
