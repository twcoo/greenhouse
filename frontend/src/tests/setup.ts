import { vi, beforeEach } from "vitest"

export const mockPush = vi.fn()
export const mockReplace = vi.fn()

vi.mock("vue-router", async (importOriginal) => {
  const actual = await importOriginal<typeof import("vue-router")>()
  return {
    ...actual,
    useRouter: () => ({
      push: mockPush,
      replace: mockReplace,
    }),
    useRoute: () => ({
      params: {},
      query: {},
    }),
  }
})

beforeEach(() => {
  mockPush.mockClear()
  mockReplace.mockClear()
})
