```js
//vite.config.js的配置，可以同时用三个不同的后端
import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    proxy: {
      // FastAPI 的后端
      '/api': {
        target: 'http://127.0.0.1:8001',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
      // Go 的后端
      '/goapi': {
        target: 'http://127.0.0.1:8083',
        changeOrigin: true,
        // 如果 Go 后端的路由就是 /api/password，就不改写
        rewrite: (path) => path.replace(/^\/goapi/, '/api'),
      },
      '/nodeapi': {
        target: 'http://127.0.0.1:3001',
        changeOrigin: true,
        // 不改写，直接保持 /nodeapi 前缀
      },
    },
  },
})


```