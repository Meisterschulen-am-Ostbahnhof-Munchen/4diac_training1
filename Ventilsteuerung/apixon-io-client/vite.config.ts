import { defineConfig } from 'vite'
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
      input: 'apixon-io.html',
    },
  },
})
