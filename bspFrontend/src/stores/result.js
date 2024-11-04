import { defineStore } from 'pinia'

export const useTestResultsStore = defineStore('testResults', {
  state: () => ({
    testIds: []
  }),
  actions: {
    addTestId(testId) {
      this.testIds.push(testId)
    },
    clearTestIds() {
      this.testIds = []
    }
  },
  getters: {
    getAllTestIds: (state) => state.testIds
  }
})
