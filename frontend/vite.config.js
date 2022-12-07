import { defineConfig } from 'vite'
import * as path from 'path';
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  server: {
    port: '3000',
  },
  plugins: [vue()],
  root: "./",
  base: "/",
  publicDir: "public",
  build: {
    outDir: "../dist",
    assetsDir: "static"
  },
  exclude: ['vue/multi-word-component-names', 'vue/script-setup-uses-vars'],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
      '/@': path.resolve(__dirname, 'resources'),
    },
  },
});
