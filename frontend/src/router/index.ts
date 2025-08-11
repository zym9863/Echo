import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

// 路由配置
const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/time-capsules',
    name: 'TimeCapsules',
    component: () => import('../views/TimeCapsules.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/time-capsules/create',
    name: 'CreateTimeCapsule',
    component: () => import('../views/CreateTimeCapsule.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/time-capsules/:id',
    name: 'TimeCapsuleDetail',
    component: () => import('../views/TimeCapsuleDetail.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/echo-wall',
    name: 'EchoWall',
    component: () => import('../views/EchoWall.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/echo-gallery',
    name: 'EchoGallery',
    component: () => import('../views/EchoGallery.vue')
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Profile.vue'),
    meta: { requiresAuth: true }
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // 需要认证的路由
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  }
  // 需要游客身份的路由（登录/注册页）
  else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/')
  }
  else {
    next()
  }
})

export default router