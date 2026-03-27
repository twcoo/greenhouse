export function toTitleCase(str: string): string {
  return (
    str
      // replace underscores with spaces
      .replace(/_/g, " ")
      // capitalize first letter of each word
      .replace(/\b\w/g, (char) => char.toUpperCase())
  )
}
