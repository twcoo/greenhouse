import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router"
import { useSetupStore } from "@/stores/setupStore"
import { useAuthStore } from "@/stores/authStore"

const routes: RouteRecordRaw[] = [
  {
    path: "/setup",
    name: "setup",
    component: () => import("@/views/setup/index.vue"),
  },
  {
    path: "/login",
    name: "login",
    component: () => import("@/views/login/index.vue"),
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: () => import("@/views/dashboard/index.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/crops",
    name: "crops",
    component: () => import("@/views/crops/index.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/planting-locations",
    name: "planting-locations",
    component: () => import("@/views/planting-locations/index.vue"),
    meta: { requiresAuth: true },
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
  const authStore = useAuthStore()

  await setupStore.checkSetup()

  // Redirect to setup if setup is required
  if (setupStore.setupRequired && to.name !== "setup") return { name: "setup" }

  // Prevent going back to setup if already completed
  if (!setupStore.setupRequired && to.name === "setup") return { name: "login" }

  // Prevent accessing login if already authenticated
  if (authStore.isAuthenticated && to.name === "login") return { name: "dashboard" }

  // Redirect to login when accessing routes while unauthenticated
  if (to.meta.requiresAuth && !authStore.isAuthenticated) return { name: "login" }

  return true
})

export default router
