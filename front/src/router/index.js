import { createRouter, createWebHistory } from 'vue-router'
import { apiService } from '@/services/api'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginView.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/RegisterView.vue')
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/MainView.vue')
  },
  {
    path: '/analytics',
    name: 'Analytics',
    component: () => import('../views/AnalyticsView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})


router.beforeEach((to, from, next) => {
  const isAuthenticated = apiService.isAuthenticated()

  console.log(`🛡️ Навигация: ${from.path} → ${to.path}, Авторизован: ${isAuthenticated}`);

  if (to.meta.requiresAuth && !isAuthenticated) {
    console.log('❌ Доступ запрещен, перенаправляем на /login');
    next('/login')
  } else if ((to.path === '/login' || to.path === '/register') && isAuthenticated) {
    console.log('🔃 Уже авторизован, перенаправляем на главную');
    next('/')
  } else {
    console.log('✅ Доступ разрешен');
    next()
  }
})

export default router