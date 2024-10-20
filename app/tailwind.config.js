/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/*.html",
    "./app/templates/**/*.html",
    "./app/templates/**/*.js",
    "./app/templates/items/*.html",
    "./app/static/dist/js/*.js",
  ],
  theme: {
    extend: {
      backgroundImage: {
        'food-patterns': "url('/app/static/dist/login.png')",
        'food-patterns2': "url('/app/static/dist/admin-login.png')",
      },
    },
  },
  plugins: [],
}

