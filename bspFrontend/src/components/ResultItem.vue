<template>
  <div class="result-item my-3">
    <div class="card mb-3 flex-fill">
      <div class="card-body">
        <h5 class="card-title">{{ testName }}</h5>
        <p class="text-muted mb-3">{{ description }}</p>
        <div class="progress mb-1" style="height: 25px">
          <div class="progress-bar" :class="labelClass(0)" role="progressbar" style="width: 33.33%">
            {{ localizedText.healthy || 'Healthy' }}
          </div>
          <div class="progress-bar" :class="labelClass(1)" role="progressbar" style="width: 33.33%">
           {{ localizedText.mild || 'Mild AD' }}
          </div>
          <div class="progress-bar" :class="labelClass(2)" role="progressbar" style="width: 33.33%">
            {{ localizedText.moderate || 'Moderate AD' }}
          </div>
        </div>
        <div class="progress" style="height: 20px">
          <div class="progress-bar" role="progressbar" :style="{ width: resultPercentage }">
            <span class="fw-bold">{{ (resultScore * 100).toFixed(2) }}%</span>
          </div>
        </div>
        <div class="d-flex justify-content-between align-items-center mt-2">
          <span>{{ timeTaken }}s</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed , onMounted} from 'vue'
const localizedText = ref({
  healthy: '',
  mild: '',
  moderate: ''
})

// On mounted, fetch the localized version of "Step"
onMounted(() => {
  getLocalization('Healthy', 'healthy')
  getLocalization('Mild AD', 'mild')
  getLocalization('Moderate AD', 'moderate')
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


// Props passed to the component
const props = defineProps({
  testName: String,
  description: String,
  labelIndex: Number,
  resultScore: Number,
  timeTaken: Number
})

// Function to determine the class of the progress bar based on label index
const labelClass = (index) => {
  if (index === props.labelIndex) {
    switch (index) {
      case 0:
        return 'bg-success' // Healthy
      case 1:
        return 'bg-warning' // Mild AD
      case 2:
        return 'bg-danger' // Moderate AD
    }
  }
  return 'bg-secondary' // non-highlighted segments
}

const resultPercentage = computed(() => `${(props.resultScore * 100).toFixed(2)}%`)
</script>

<style scoped></style>
