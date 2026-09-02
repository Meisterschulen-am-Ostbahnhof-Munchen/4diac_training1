import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
import { viteSingleFile } from 'vite-plugin-singlefile'

export default defineConfig({
  plugins: [vue(), viteSingleFile()],
  define: {
    global: 'globalThis',
  },
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: 'apixon-ai-calibrate.html',
    },
  },
  test: {
    environment: 'jsdom',
    coverage: {
      provider: 'v8',
      reporter: ['cobertura'],
      reportsDirectory: 'coverage',
    },
  },
})
