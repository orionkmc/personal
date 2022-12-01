import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  root: "./",
  base: "/",
  publicDir: "public",
  build: {
    outDir: "../dist",
    assetsDir: "static"
  },
  plugins: [vue()]
});
