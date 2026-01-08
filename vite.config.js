import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 5173,
    open: true,
    proxy: {
      // 开发环境代理，解决 CORS 问题
      '/api/coros': {
        target: 'https://coros.redeyes.top',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/coros/, '')
      }
    }
  }
})
