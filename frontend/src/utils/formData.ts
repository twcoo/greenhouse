export function toFormData<T extends object>(obj: T): FormData {
  const fd = new FormData()
  for (const [key, value] of Object.entries(obj)) {
    if (value === null || value === undefined) continue
    if (value instanceof File) {
      fd.append(key, value)
      continue
    }
    fd.append(key, String(value))
  }
  return fd
}
