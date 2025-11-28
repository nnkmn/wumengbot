import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/player',
      name: 'player',
      component: () => import('../views/PlayerView.vue')
    },
    {
      path: '/scores',
      name: 'scores',
      component: () => import('../views/ScoresView.vue')
    },
    {
      path: '/songs',
      name: 'songs',
      component: () => import('../views/SongsView.vue')
    },
    {
      path: '/plates',
      name: 'plates',
      component: () => import('../views/PlatesView.vue')
    }
  ]
})

export default router
