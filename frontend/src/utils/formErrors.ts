import type { ZodError } from "zod"

export function zodToFormErrors(error: ZodError): Record<string, string> {
  const errors: Record<string, string> = {}

  for (const issue of error.issues) {
    const field = issue.path[0] as string
    errors[field] = issue.message
  }

  return errors
}

export function apiToFormErrors(
  apiErrors: Record<string, string[]> | string,
): Record<string, string> {
  const errors: Record<string, string> = {}

  if (typeof apiErrors == "string") {
    errors.general = apiErrors
    return errors
  }

  for (const key in apiErrors) {
    errors[key] = apiErrors[key][0]
  }

  return errors
}
