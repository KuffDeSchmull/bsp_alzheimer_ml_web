import { defineStore } from 'pinia'

export const useTestStore = defineStore('test', {
  state: () => ({
    tests: [], // Array of tests
    currentTestIndex: 0,
    currentStep: 0,
    inputMethod: null, // 'canvas' or 'import'
    testResults: {} // Stores results for each test
  }),

  getters: {
    currentTest: (state) => {
      return state.tests[state.currentTestIndex] || { name: '', steps: [] }
    },
    totalSteps: (state) => {
      return state.tests.reduce((sum, test) => sum + test.steps.length, 2)
    }
  },

  actions: {
    chooseInputMethod(method) {
      this.inputMethod = method
    },
    goToNextStep() {
      // Logic to move to the next step
      if (this.currentStep < this.totalSteps - 1) {
        this.currentStep++
      } else {
        this.currentStep = 0
        this.currentTestIndex = (this.currentTestIndex + 1) % this.tests.length //go to next test
      }
    },
    handleCanvasStep(step) {
      // Logic for handling a canvas drawing step
    },
    handlePhysicalStep(step) {
      // Logic for handling a physical drawing step
    },
    handleImportStep(step) {
      // Logic for handling an import step
    },
    saveTestResult(testId, result) {
      this.testResults[testId] = result
    }
    // Additional actions as needed
  }
})
