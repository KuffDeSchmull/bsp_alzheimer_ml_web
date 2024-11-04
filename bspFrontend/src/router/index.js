import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import CreateUser from '../views/CreateUser.vue'
import Login from '../views/Login.vue'
import Condition from '../views/Condition.vue'
import ChooseTests from '../views/ChooseTests.vue'
import Profile from '../views/Profile.vue'
import CanvasTest from '../views/CanvasTest.vue'
import Results from '../views/ResultView.vue'
import InputMethod from '../views/InputMethod.vue'
import Import from '../views/Import.vue'
import DrawPrompt from '../views/DrawPrompt.vue'

import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/conditions',
      name: 'conditions',
      component: Condition
    },
    {
      path: '/choosetests',
      name: 'choosetests',
      component: ChooseTests
    },
    {
      path: '/administration',
      name: 'administration',
      component: Profile
    },
    {
      path: '/canvas',
      name: 'canvas',
      component: CanvasTest
    },
    {
      path: '/results',
      name: 'results',
      component: Results
    },
    {
      path: '/register',
      name: 'register',
      component: CreateUser
    },
    {
      path: '/input',
      name: 'InputMethod',
      component: InputMethod
    },
    {
      path: '/import',
      name: 'Import',
      component: Import
    },
    {
      path: '/draw',
      name: 'Draw',
      component: DrawPrompt
    }
  ]
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  var auth = 0
  if (sessionStorage.getItem('isAuthenticated')) {
    auth = parseInt(sessionStorage.getItem('isAuthenticated'))
  } else {
    auth = 0
  }

  if (to.path !== '/login' && to.path !== '/register' && auth == 0) {
    // If the user is not authenticated and is trying to access a non-login page
    next('/login')
  } else if ((to.path === '/login' || to.path === '/register') && auth == 1) {
    // If the user is authenticated and is trying to access the login page
    next('/') // Redirect to home or another appropriate route
  } else {
    // Otherwise, allow the navigation
    next()
  }
})

export default router
