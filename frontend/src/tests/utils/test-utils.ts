import { vi } from "vitest"
import { useAuthStore } from "@/stores/authStore"

export const createAuthStoreMock = (overrides = {}): ReturnType<typeof useAuthStore> =>
  ({
    user: { username: "krubus" },
    isAuthenticated: true,
    isLoading: false,
    error: null,
    login: vi.fn(),
    logout: vi.fn().mockResolvedValue(undefined),
    clearAuth: vi.fn(),
    ...overrides,
  }) as unknown as ReturnType<typeof useAuthStore>
