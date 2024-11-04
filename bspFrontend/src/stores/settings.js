import { defineStore } from 'pinia'

export const useAccessibilityStore = defineStore('accessibility', {
  state: () => ({
    useLargeFont: false,
    useSerifFont: false,
    highContrast: false
  }),
  actions: {
    toggleLargeFont() {
      this.useLargeFont = !this.useLargeFont
    },
    toggleSerifFont() {
      this.useSerifFont = !this.useSerifFont
    },
    toggleHighContrast() {
      this.highContrast = !this.highContrast
    }
  }
})
