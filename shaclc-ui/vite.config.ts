import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      // Alias node-fetch to isomorphic-fetch for pyodide 0.24 to work correctly.
      'node-fetch': 'isomorphic-fetch',
    }
  }
})
