import { createRouter, createWebHistory } from '@ionic/vue-router';
import { RouteRecordRaw } from 'vue-router';
import HomePage from '../views/HomePage.vue'
import DashboardPage from '@/views/DashboardPage.vue';
import TemperaturesListPage from '@/views/TemperaturesListPage.vue';
import SignupPage from '@/views/SignupPage.vue';
import PasswordPage from '@/views/PasswordPage.vue';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: HomePage
  },
  {
    path: '/signup',
    name: 'Signup',
    component: SignupPage
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardPage
  },
  {
    path: '/temperatures',
    name: 'TemperaturesList',
    component: TemperaturesListPage
  },
  {
    path: '/password',
    name: 'ForgotPassword',
    component: PasswordPage
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
