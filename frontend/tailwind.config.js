module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx}',
    './src/components/**/*.{js,ts,jsx,tsx}',
    './src/app/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        background: '#0f172a',
        foreground: '#f1f5f9',
        primary: '#3b82f6',
        secondary: '#8b5cf6',
        accent: '#ec4899',
        muted: '#64748b',
        border: '#1e293b',
      },
    },
  },
  plugins: [],
}
