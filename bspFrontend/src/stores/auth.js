import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: false //initial value
  }),
  actions: {
    updateAuthStatus(status) {
      this.isAuthenticated = status
      sessionStorage.setItem('isAuthenticated', 1)
    },
    clearLocalStorageAndLogout() {
      this.updateAuthStatus(false)
      sessionStorage.clear()
      sessionStorage.setItem('isAuthenticated', 0)
      // Additional actions like redirecting
    }
  }
})
