import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Dev: the browser calls /api/* and Vite forwards it to the FastAPI backend.
export default defineConfig({
  plugins: [react()],
  test: { environment: "jsdom", globals: true },
  server: {
    port: 5173,
    proxy: { "/api": { target: process.env.API_URL || "http://localhost:8000", rewrite: (p) => p.replace(/^\/api/, "") } },
  },
});
