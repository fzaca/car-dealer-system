/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './service/static/js/**/*.js',
    './service/static/css/styles.css',
    './resources/core/templates/*.html',
    './resources/core/templates/**/*.html'
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('daisyui'),
  ],
  daisyui: {
    themes: [
      {
        cardealer: {
          "primary": "#0064ff",      // Primary color
          "primary-focus": "#0050dc", // Primary focus color
          "primary-content": "#ffffff", // Primary content color
          "secondary": "#00f986",    // Secondary color
          "accent": "#009eff",       // Accent color
          "neutral": "#090909",      // Neutral color
          "base-100": "#28212b",     // Base color
          "info": "#00adff",         // Info color
          "success": "#43c967",      // Success color
          "warning": "#966200",      // Warning color
          "error": "#ff9b98",        // Error color
        },
      },
    ],
  },
};
