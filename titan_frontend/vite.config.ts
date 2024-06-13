import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  plugins: [react()],
  // server: {
  //   cors: false,
  //   proxy: {
  //     '/api': {
  //       target: 'https://fomac.ai',
  //       changeOrigin: true,
  //       secure: false,
  //     },
  //   },
  // },
});
