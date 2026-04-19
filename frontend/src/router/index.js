import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'dashboard',
            component: () => import('@/views/DashboardView.vue'),
        },
        {
            path: '/transactions',
            name: 'transactions',
            component: () => import('@/views/TransactionsView.vue'),
        },
        {
            path: '/categories',
            name: 'categories',
            component: () => import('@/views/CategoriesView.vue'),
        },
    ],
})

export default router