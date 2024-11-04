<script setup>
import ResultItem from '../components/ResultItem.vue'
import Footer from '@/components/Footer.vue'
import HealthNotice from '@/components/HealthNotice.vue'
import { useTestResultsStore } from '@/stores/result'

import { ref, onMounted } from 'vue'
import useAxios from '@/composables/useAxios'

const isLoading = ref(true)
const testResults = ref([])
const healthNotice = ref(null)
const currentStep = ref(parseInt(sessionStorage.getItem('currentStep'), 10) || 1)
const totalSteps = ref(parseInt(sessionStorage.getItem('totalSteps'), 10) || 0)
const testIdStore = useTestResultsStore()

const processHealthMessage = (state, percentage) => {
  if (!state) return ''
  return state.replace('<percent>', `${(percentage * 100).toFixed(2)}`)
}

onMounted(async () => {
  const axios = useAxios()
  try {
    const testIds = testIdStore.getAllTestIds
    const response = await axios.post('/api/test/evaluate', { testIds })
    testResults.value = response.data.results
    healthNotice.value = response.data.healthNotice || null
    //console.log("Health Notice:", healthNotice.value);
  } catch (error) {
    console.error('Error fetching test results:', error)
  } finally {
    testIdStore.clearTestIds()
    isLoading.value = false // Stop loading irrespective of success or failure
  }
})
</script>
<template>
  <div class="container results-container" id="mainContent">
    <div v-if="isLoading">
      <!-- Display loading screen here -->
      <p>Loading results...</p>
    </div>
    <div v-else>
      <div v-for="(result, index) in testResults" :key="index">
        <ResultItem
          :test-name="result.name"
          :description="processHealthMessage(result.state, result.percentage)"
          :label-index="result.label"
          :result-score="result.percentage"
          :time-taken="result.time"
        />
      </div>
      <!-- Display Health Notice -->
      <div v-if="healthNotice" class="notice">
        <HealthNotice :healthNotices="healthNotice" />
      </div>
    </div>
  </div>
  <Footer :currentStep="currentStep" :totalSteps="totalSteps" />
</template>

<style>
.results-container {
  padding-bottom: 10em;
}
</style>
