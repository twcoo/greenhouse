import { describe, it, expect } from "vitest"
import { setupAdminSchema } from "@/schemas/setup.schema"

describe("setupAdminSchema", () => {
  describe("valid data", () => {
    it("accepts valid username and matching passwords", () => {
      const result = setupAdminSchema.safeParse({
        username: "admin",
        password: "password123",
        password2: "password123",
      })
      expect(result.success).toBe(true)
    })
  })

  describe("username validation", () => {
    it("rejects username shorter than 3 characters", () => {
      const result = setupAdminSchema.safeParse({
        username: "ab",
        password: "password123",
        password2: "password123",
      })
      expect(result.success).toBe(false)
      if (!result.success) {
        const fields = result.error.issues.map((i) => i.path[0])
        expect(fields).toContain("username")
      }
    })

    it("rejects username longer than 30 characters", () => {
      const result = setupAdminSchema.safeParse({
        username: "a".repeat(31),
        password: "password123",
        password2: "password123",
      })
      expect(result.success).toBe(false)
      if (!result.success) {
        const fields = result.error.issues.map((i) => i.path[0])
        expect(fields).toContain("username")
      }
    })
  })

  describe("password validation", () => {
    it("rejects password shorter than 8 characters", () => {
      const result = setupAdminSchema.safeParse({
        username: "admin",
        password: "short",
        password2: "short",
      })
      expect(result.success).toBe(false)
      if (!result.success) {
        const fields = result.error.issues.map((i) => i.path[0])
        expect(fields).toContain("password")
      }
    })
  })

  describe("password confirmation", () => {
    it("rejects mismatched passwords", () => {
      const result = setupAdminSchema.safeParse({
        username: "admin",
        password: "password123",
        password2: "different123",
      })
      expect(result.success).toBe(false)
      if (!result.success) {
        const fields = result.error.issues.map((i) => i.path[0])
        expect(fields).toContain("password2")
      }
    })
  })
})
