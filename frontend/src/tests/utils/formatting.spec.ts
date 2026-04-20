import { describe, it, expect } from "vitest"
import { toTitleCase } from "@/utils/formatting"

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
