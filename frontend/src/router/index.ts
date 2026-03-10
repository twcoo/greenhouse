import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router"

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
    path: "/signup",
    name: "signup",
    component: () => import("@/views/signup/index.vue"),
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

export default router
