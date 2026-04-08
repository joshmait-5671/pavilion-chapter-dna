import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Pavilion Brand
        'pav-pink': { DEFAULT: '#DF285B', 100: '#FEF9F9', 200: '#FFEDF2', 400: '#C57FD9', 600: '#F13472', 700: '#DF285B', 800: '#B81C48' },
        'pav-blue': { DEFAULT: '#180A5C', 100: '#EDEAFF', 200: '#CEC5F4', 400: '#6D69CF', 500: '#432CAE', 600: '#2B1887', 700: '#180A5C', 800: '#0D0039' },
        'pav-purple': { DEFAULT: '#59146C', 400: '#C57FD9', 600: '#7F2A97', 700: '#59146C' },
        // Functional
        canvas: '#180A5C',
        card: 'rgba(255,255,255,0.08)',
        'card-hover': 'rgba(255,255,255,0.12)',
        'card-selected': 'rgba(255,255,255,0.15)',
        'card-light': '#F9F8FF',
        border: 'rgba(255,255,255,0.12)',
        'border-selected': '#DF285B',
        primary: '#FFFFFF',
        muted: 'rgba(255,255,255,0.5)',
        track: 'rgba(255,255,255,0.1)',
      },
      fontFamily: {
        sans: ['var(--font-inter)', 'system-ui', 'sans-serif'],
        display: ['var(--font-poppins)', 'system-ui', 'sans-serif'],
      },
      animation: {
        'slide-in': 'slideIn 0.28s cubic-bezier(0.16, 1, 0.3, 1) forwards',
        'fade-in': 'fadeIn 0.2s ease forwards',
      },
      keyframes: {
        slideIn: {
          from: { transform: 'translateY(12px)', opacity: '0' },
          to: { transform: 'translateY(0)', opacity: '1' },
        },
        fadeIn: {
          from: { opacity: '0' },
          to: { opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}

export default config
