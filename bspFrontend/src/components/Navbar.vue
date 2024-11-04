<script setup>
import { RouterLink } from 'vue-router'
import { onUnmounted, ref, onMounted} from 'vue'
// Create a reactive reference for the authentication status
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const localizedText = ref({
  login: '',
  home: '',
  administration: ''
})

// On mounted, fetch the localized version of "Step"
onMounted(() => {
  getLocalization('Login', 'login')
  getLocalization('Home', 'home')
  getLocalization('Administration', 'administration')
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

</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <a class="navbar-brand">
        <img src="@/assets/logo.svg" alt="Logo" class="d-inline-block align-top logo-svg" />
        <!-- Replace with your SVG path -->
        <span class="brand-text">ML Screening</span>
      </a>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNavAltMarkup"
        aria-controls="navbarNavAltMarkup"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-end" id="navbarNavAltMarkup">
        <div class="navbar-nav flex-column flex-lg-row mt-4">
          <RouterLink
            v-if="!authStore.isAuthenticated"
            class="nav-item btn btn-outline-primary me-3 mb-2 mb-lg-0 me-lg-3"
            to="/login"
            >{{ localizedText.login || 'Login' }}</RouterLink
          >
          <RouterLink
            v-if="authStore.isAuthenticated"
            class="nav-item btn btn-outline-primary me-3 mb-2 mb-lg-0 me-lg-3"
            to="/"
            >{{ localizedText.home || 'Home' }}</RouterLink
          >
          <RouterLink
            v-if="authStore.isAuthenticated"
            class="nav-item btn btn-outline-primary me-3 mb-2 mb-lg-0 me-lg-3"
            to="/administration"
            >{{ localizedText.administration || 'Administration' }}</RouterLink
          >
        </div>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.logo-svg {
  height: 1.5em; /* Adjust size as needed */
  width: auto;
  vertical-align: middle;
  margin-right: 1em;
}
#navbarNavAltMarkup {
  margin-right: 1em;
}
</style>
