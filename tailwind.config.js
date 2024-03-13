/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/*.html",
    "./templates/**/*.html",
    "./templates/**/*.js",
    "./static/stc/**/*.js",
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

