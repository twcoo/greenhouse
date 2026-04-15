import { describe, it, expect } from "vitest"
import { authLoginSchema } from "@/schemas/auth.schema"

describe("authLoginSchema", () => {
  describe("valid data", () => {
    it("accepts valid username and password", () => {
      const result = authLoginSchema.safeParse({
        username: "admin",
        password: "secret",
      })
      expect(result.success).toBe(true)
    })
  })

  describe("username validation", () => {
    it("rejects empty username", () => {
      const result = authLoginSchema.safeParse({
        username: "",
        password: "secret",
      })
      expect(result.success).toBe(false)
      if (!result.success) {
        const fields = result.error.issues.map((i) => i.path[0])
        expect(fields).toContain("username")
      }
    })
  })

  describe("password validation", () => {
    it("rejects empty password", () => {
      const result = authLoginSchema.safeParse({
        username: "admin",
        password: "",
      })
      expect(result.success).toBe(false)
      if (!result.success) {
        const fields = result.error.issues.map((i) => i.path[0])
        expect(fields).toContain("password")
      }
    })
  })
})
