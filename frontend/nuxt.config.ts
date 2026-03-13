import vuetify from 'vite-plugin-vuetify'

export default defineNuxtConfig({
  devtools: { enabled: true },

  modules: [
    '@nuxtjs/supabase',
  ],

  build: {
    transpile: ['vuetify'],
  },

  vite: {
    plugins: [
      vuetify({ autoImport: true }),
    ],
  },

  css: [
    'vuetify/styles',
    '@mdi/font/css/materialdesignicons.css',
  ],

  supabase: {
    redirectOptions: {
      login: '/login',
      callback: '/confirm',
      exclude: ['/', '/products/**'],
    },
  },

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8080',
    },
  },

  compatibilityDate: '2024-11-01',
})
