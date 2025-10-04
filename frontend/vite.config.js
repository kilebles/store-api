import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const isDocker = process.env.DOCKER === "true";

export default defineConfig({
  plugins: [react({ jsxRuntime: "automatic" })],
  server: {
    host: "0.0.0.0",
    port: 3000,
    proxy: {
      "/api": {
        target: isDocker ? "http://backend:8000" : "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
});