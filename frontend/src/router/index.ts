import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/Home.vue'),
    },
    {
      path: '/bazi',
      name: 'bazi',
      component: () => import('@/views/BaziPage.vue'),
    },
    {
      path: '/ziwei',
      name: 'ziwei',
      component: () => import('@/views/ZiweiPage.vue'),
    },
    {
      path: '/liuyao',
      name: 'liuyao',
      component: () => import('@/views/LiuyaoPage.vue'),
    },
    {
      path: '/result/:id?',
      name: 'result',
      component: () => import('@/views/ResultPage.vue'),
    },
    {
      path: '/history',
      name: 'history',
      component: () => import('@/views/HistoryPage.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/Login.vue'),
    },
  ],
})

export default router
