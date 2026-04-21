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
    path: "/varieties",
    name: "varieties",
    component: () => import("@/views/varieties/index.vue"),
    meta: { requiresAuth: true },
  },

  {
    path: "/service-unavailable",
    name: "service-unavailable",
    component: () => import("@/views/service-unavailable/index.vue"),
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

type RouteName = "service-unavailable" | "setup" | "login" | "dashboard"
type Redirect = { name: RouteName }
type RouteContext = {
  to: { name: string | symbol | null | undefined; meta: { requiresAuth?: boolean } }
  setupStore: ReturnType<typeof useSetupStore>
  authStore: ReturnType<typeof useAuthStore>
}

function backendGuard({ to, setupStore, authStore }: RouteContext): Redirect | null {
  if (setupStore.backendUnavailable && to.name !== "service-unavailable") {
    return { name: "service-unavailable" }
  }
  if (!setupStore.backendUnavailable && to.name === "service-unavailable") {
    return authStore.isAuthenticated ? { name: "dashboard" } : { name: "login" }
  }
  return null
}

function setupGuard({ to, setupStore }: RouteContext): Redirect | null {
  if (setupStore.setupRequired && to.name !== "setup") return { name: "setup" }
  if (!setupStore.setupRequired && to.name === "setup") return { name: "login" }
  return null
}

function authGuard({ to, authStore }: RouteContext): Redirect | null {
  if (authStore.isAuthenticated && to.name === "login") return { name: "dashboard" }
  if (to.meta.requiresAuth && !authStore.isAuthenticated) return { name: "login" }
  return null
}

router.beforeEach(async (to) => {
  const setupStore = useSetupStore()
  const authStore = useAuthStore()

  await setupStore.checkSetup()

  const ctx: RouteContext = { to, setupStore, authStore }
  return backendGuard(ctx) ?? setupGuard(ctx) ?? authGuard(ctx) ?? true
})

export default router
