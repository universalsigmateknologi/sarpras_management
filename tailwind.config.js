/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./**/templates/**/*.html",
  ],
  theme: {
    extend: {
        fontFamily: {
            display: ['Sora', 'sans-serif'],
            body: ['DM Sans', 'sans-serif'],
        },
        colors: {
            surface: '#FAFAFA',
            ink: '#0F0F0F',
            muted: '#999999',
            faint: '#E8E8E8',
            subtle: '#F3F3F3',
        }
    }
  },
  plugins: [],
}