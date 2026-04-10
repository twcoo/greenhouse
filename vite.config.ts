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
    globals: true
  },
})

export default {
  ...config,
  ...tstConfig,
}
