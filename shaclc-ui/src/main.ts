import './assets/main.css'

import { createApp } from 'vue'
import PrimeVue from 'primevue/config'
import ToastService from 'primevue/toastservice'
import Lara from '@/presets/lara'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(PrimeVue, {
  unstyled: true,
  pt: Lara
})
app.use(ToastService)
app.use(router)
app.mount('#app')
