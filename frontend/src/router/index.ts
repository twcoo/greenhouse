import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router"
import { useSetupStore } from "@/stores/setupStore"

const routes: RouteRecordRaw[] = [
  {
    path: "/login",
    name: "login",
    component: () => import("@/views/login/index.vue"),
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: () => import("@/views/dashboard/index.vue"),
  },
  {
    path: "/setup",
    name: "setup",
    component: () => import("@/views/setup/index.vue"),
  },
  {
    path: "/",
    redirect: "/login",
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to) => {
  const setupStore = useSetupStore()
  await setupStore.checkSetup()

  if (setupStore.setupRequired && to.name !== "setup") return { name: "setup" }
  if (!setupStore.setupRequired && to.name === "setup") return { name: "login" }

  return true
})

export default router
