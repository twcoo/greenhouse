import path from 'node:path'
import { defineConfig as testConfig } from "vitest/config";
import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import vue from '@vitejs/plugin-vue'

const config = defineConfig({
  root: "frontend",
  plugins: [vue(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './frontend/src'),
    }
  }
})

const tstConfig = testConfig({
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./frontend/src/tests/setup.ts"],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      include: ['frontend/src/**/*.{ts,vue}'],
      exclude: ['frontend/src/tests/**', 'frontend/src/main.ts', 'frontend/src/components/ui/**'],
      thresholds: {
        lines: 80,
        functions: 70,
      },
    },
  },
})

export default {
  ...config,
  ...tstConfig,
}
