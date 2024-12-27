/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./order/**/*.html"],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('preline/plugin'),
  ],
}

