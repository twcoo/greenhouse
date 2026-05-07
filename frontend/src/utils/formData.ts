import { decamelize } from "humps"

export function toFormData<T extends object>(obj: T): FormData {
  const fd = new FormData()
  for (const [key, value] of Object.entries(obj)) {
    if (value === null || value === undefined) continue
    if (value instanceof File) {
      fd.append(decamelize(key), value)
      continue
    }
    fd.append(decamelize(key), String(value))
  }
  return fd
}

export function getFileFromEvent(event: Event): File | undefined {
  return (event.target as HTMLInputElement).files?.[0]
}
