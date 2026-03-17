import { describe, it, expect } from "vitest"
import { z } from "zod"
import { zodToFormErrors, apiToFormErrors } from "@/utils/formErrors"

describe("zodToFormErrors", () => {
  it("maps single field error", () => {
    const schema = z.object({
      username: z.string().min(3, "Too short")
    })

    const result = schema.safeParse({ username: "" })

    if (!result.success) {
      const errors = zodToFormErrors(result.error)

      expect(errors).toEqual({
        username: "Too short"
      })
    }
  })

  it("maps multiple field errors", () => {
    const schema = z.object({
      username: z.string().min(3, "Too short"),
      password: z.string().min(8, "Too weak")
    })

    const result = schema.safeParse({
      username: "",
      password: "123"
    })

    if (!result.success) {
      const errors = zodToFormErrors(result.error)

      expect(errors).toEqual({
        username: "Too short",
        password: "Too weak"
      })
    }
  })
})

describe("apiToFormErrors", () => {
  it("handles string error as general", () => {
    const result = apiToFormErrors("Something went wrong")

    expect(result).toEqual({
      general: "Something went wrong"
    })
  })

  it("maps API field errors (first message only)", () => {
    const apiErrors = {
      username: ["Already exists", "Another error"],
      password: ["Too short"]
    }

    const result = apiToFormErrors(apiErrors)

    expect(result).toEqual({
      username: "Already exists",
      password: "Too short"
    })
  })

  it("handles empty object", () => {
    const result = apiToFormErrors({})

    expect(result).toEqual({})
  })
})
