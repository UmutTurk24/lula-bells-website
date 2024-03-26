/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/*.html",
    "./templates/**/*.html",
    "./templates/**/*.js",
    "./templates/items/*.html",
    "./static/dist/js/*.js",
  ],
  theme: {
    extend: {
      backgroundImage: {
        'food-patterns': "url('/static/dist/login.png')",
      },
    },
  },
  plugins: [],
}

