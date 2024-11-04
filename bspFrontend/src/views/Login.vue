<script setup>
import { useAuthStore } from '@/stores/auth'
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import { useValidation } from '@/composables/validation'
import { onMounted, onUnmounted } from 'vue'

const localizedText = ref({
  login: '',
  register: '',
  name: '',
  surname: '',
  password: ''
})


// Localization method
async function getLocalization(defaultText, key) {
  try {
    const response = await fetch('/api/test/getlocalization', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'language': sessionStorage.getItem('language')
      },
      body: JSON.stringify({ default: defaultText })
    })

    if (response.ok) {
      const result = await response.json()
      localizedText.value[key] = result.translation
    } else {
      console.error('Failed to fetch localization')
    }
  } catch (error) {
    console.error('Error fetching localization:', error)
  }
}

onMounted(() => {
  getLocalization('Login', 'login')
  getLocalization('Register', 'register')
  getLocalization('Name', 'name')
  getLocalization('Surname', 'surname')
  getLocalization('Password', 'password')
  const meta = document.createElement('meta')
  meta.name = 'viewport'
  meta.content = 'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no'
  document.getElementsByTagName('head')[0].appendChild(meta)
})

onUnmounted(() => {
  const metas = document.getElementsByTagName('meta')
  for (let i = 0; i < metas.length; i++) {
    if (metas[i].getAttribute('name') === 'viewport') {
      metas[i].parentNode.removeChild(metas[i])
    }
  }
})

const authStore = useAuthStore()
const router = useRouter()
const val = useValidation()
const userStore = useUserStore()
const errorMessage = ref('')

const loginDetails = ref({
  name: '',
  surname: '',
  password: ''
})



const loginUser = async () => {
  console.log('whats up?')
  try {
    const response = await fetch('/api/user/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(loginDetails.value)
    })
    if (response.status === 401) {
      // Handle 401 Unauthorized
      errorMessage.value = 'Incorrect username or password.'
      return
    }
    if (!response.ok) {
      throw new Error('Failed to login')
    }

    const data = await response.json()
    userStore.setSessionId(data.session_id)
    sessionStorage.setItem('session_id', data.session_id)
    sessionStorage.setItem('name', loginDetails.value.name) // Storing user's name
    sessionStorage.setItem('surname', loginDetails.value.surname) // Storing user's surname
    authStore.updateAuthStatus(true)
    // store session ID, update auth state
    console.log('Login successful:', data)
    router.push('/')
  } catch (error) {
    errorMessage.value = error.message
  }
}

const redirectToRegister = () => {
  router.push({
    path: '/register',
    query: { name: loginDetails.value.name, surname: loginDetails.value.surname }
  })
}
</script>

<template>
  <div class="container login-container" id="mainContent">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{{ localizedText.login || 'Login' }}</h5>
            <form @submit.prevent="loginUser" class="login-form">
              <div class="mb-3">
                <label for="loginName" class="form-label">{{ localizedText.name || 'Name' }}</label>
                <input
                  type="text"
                  class="form-control"
                  id="loginName"
                  v-model="loginDetails.name"
                />
              </div>
              <div class="mb-3">
                <label for="loginSurname" class="form-label">{{ localizedText.surname || 'Surname' }}</label>
                <input
                  type="text"
                  class="form-control"
                  id="loginSurname"
                  v-model="loginDetails.surname"
                />
              </div>
              <div class="mb-3">
                <label for="loginPassword" class="form-label">{{ localizedText.password || 'Password' }}</label>
                <input
                  type="password"
                  class="form-control"
                  id="loginPassword"
                  v-model="loginDetails.password"
                />
              </div>
              <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>
              <button type="submit" class="btn btn-primary">{{ localizedText.login || 'Login' }}</button>
              <button type="button" class="btn btn-secondary" @click="redirectToRegister">
                {{ localizedText.register || 'Register' }}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
/* Add your styles here */
.section {
  padding-top: 2em;
}
.conditionalElement {
  padding-top: 0.5em;
}
.login-container {
  margin-top: 5vh;
}
.login-form {
  margin-top: 2em;
}
.btn {
  margin-right: 1em;
}
</style>
