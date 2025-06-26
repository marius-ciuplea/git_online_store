// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // Doar șabloanele HTML din aplicația ta 'core'
    './core/templates/core/**/*.html',
    // Dacă ai șabloane și în rădăcina proiectului (adică /app/templates/*.html)
    './templates/**/*.html',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}