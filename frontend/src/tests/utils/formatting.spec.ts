import { describe, it, expect } from "vitest"
import { formatDate, toTitleCase } from "@/utils/formatting"

describe("formatDate", () => {
  it("formats an ISO date string into a readable date", () => {
    const result = formatDate("2024-03-01T00:00:00Z")
    expect(result).toBeTruthy()
    expect(result).not.toBe("—")
  })

  it("returns the default fallback '—' when value is null", () => {
    expect(formatDate(null)).toBe("—")
  })

  it("returns a custom fallback when value is null", () => {
    expect(formatDate(null, "Present")).toBe("Present")
  })
})

describe("toTitleCase", () => {
  it("returns empty string for empty input", () => {
    expect(toTitleCase("")).toBe("")
  })

  it("capitalizes a single word", () => {
    expect(toTitleCase("hello")).toBe("Hello")
  })

  it("capitalizes multiple words", () => {
    expect(toTitleCase("hello world")).toBe("Hello World")
  })

  it("splits camelCase into separate words", () => {
    expect(toTitleCase("helloWorld")).toBe("Hello World")
  })

  it("replaces underscores with spaces", () => {
    expect(toTitleCase("hello_world")).toBe("Hello World")
  })

  it("handles mixed underscores and camelCase", () => {
    expect(toTitleCase("my_fieldName")).toBe("My Field Name")
  })
})
