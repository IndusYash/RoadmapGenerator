/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      colors: {
        // True black system palette
        surface: {
          DEFAULT: '#0d0d0d',
          raised: '#111111',
          overlay: '#161616',
          subtle: '#1a1a1a',
        },
        border: {
          DEFAULT: '#232323',
          subtle: '#1c1c1c',
          strong: '#2e2e2e',
        },
        text: {
          primary: '#e4e4e7',
          secondary: '#a1a1aa',
          muted: '#52525b',
          disabled: '#3f3f46',
        },
        accent: {
          DEFAULT: '#e4e4e7',
          dim: '#71717a',
        },
      },
      maxWidth: {
        '8xl': '88rem',
      },
      keyframes: {
        fadeIn: {
          from: { opacity: '0', transform: 'translateY(10px)' },
          to:   { opacity: '1', transform: 'translateY(0)' },
        },
        dotBounce: {
          '0%, 80%, 100%': { transform: 'scale(0.5)', opacity: '0.3' },
          '40%':            { transform: 'scale(1.1)', opacity: '1' },
        },
      },
      animation: {
        fadeIn: 'fadeIn 0.35s ease-out both',
        dotBounce: 'dotBounce 1.4s ease-in-out infinite',
      },
    },
  },
  plugins: [],
};
