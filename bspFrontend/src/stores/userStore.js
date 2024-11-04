// userStore.js
import { defineStore } from 'pinia'

export const useUserStore = defineStore('userStore', {
  state: () => ({
    sessionId: null
  }),
  actions: {
    setSessionId(sessionId) {
      this.sessionId = sessionId
    }
  }
})
