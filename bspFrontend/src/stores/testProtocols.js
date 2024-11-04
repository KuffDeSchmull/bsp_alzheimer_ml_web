// stores/testProtocolStore.js
import { defineStore } from 'pinia'

export const useTestProtocolStore = defineStore('testProtocol', {
  state: () => ({
    protocol: null,
    currentTaskIndex: 0,
    currentStepIndex: 0,
    cumulativeStepIndex: 0
  }),
  getters: {
    currentTask: (state) => state.protocol?.tasks[state.currentTaskIndex - 1],
    isCnnTest: (state) => state.protocol?.tasks[state.currentTaskIndex]?.type.includes('cnn'),
    totalTasks: (state) => state.protocol?.tasks.length || 0,
    protocolName: (state) => state.protocol?.type
  },
  actions: {
    setProtocol(protocol) {
      this.protocol = protocol
      this.currentTaskIndex = 1
      this.currentStepIndex = 0
      this.cumulativeStepIndex = 0
    },
    nextTask() {
      if (this.currentTaskIndex < this.totalTasks) {
        this.currentTaskIndex++
        this.currentStepIndex = 0 // Reset step index for new task
        this.cumulativeStepIndex++
      } else {
        console.log('request results')
      }
      console.log(this.currentTaskIndex)
      console.log(this.totalTasks)
    },
    nextStep() {
      sessionStorage.setItem('currentStep', parseInt(sessionStorage.getItem('currentStep')) + 1)
      if (this.isCnnTest && this.currentStepIndex < 1) {
        this.currentStepIndex++
        this.cumulativeStepIndex++
        console.log(this.currentTaskIndex)
      } else {
        this.nextTask() // Move to next task if steps are completed for current task
      }
    },
    resetProtocol() {
      this.protocol = null
      this.currentTaskIndex = 0
      this.currentStepIndex = 0
      this.cumulativeStepIndex = 0
      sessionStorage.setItem('currentStep', 0)
      sessionStorage.setItem('totalSteps', 0)
    }
  }
})
