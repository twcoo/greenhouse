import { createApp } from "vue"
import { createPinia } from "pinia"
import "@/style.css"
import App from "@/App.vue"
import router from "@/router"
import { VueQueryPlugin, type VueQueryPluginOptions } from '@tanstack/vue-query'

const pinia = createPinia()
const app = createApp(App)

const vueQueryOptions: VueQueryPluginOptions = {
  queryClientConfig: {
    defaultOptions: {
      queries: {
        refetchOnWindowFocus: false,
        retry: 1,
      },
    },
  },
}

app.use(VueQueryPlugin, vueQueryOptions)
app.use(pinia)
app.use(router)
app.mount("#app")
