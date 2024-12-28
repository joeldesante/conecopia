/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./order/**/*.html"],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Montserrat"', 'sans-serif'],
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('preline/plugin'),
  ],
}

