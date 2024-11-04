<template>
  <div class="container-fluid footer">
    <div class="footer-nav row justify-content-center align-items-center">
      <!-- Use Bootstrap flex utilities to align dots horizontally -->
      <div class="footer-item step d-flex flex-row justify-content-center align-items-center">
        <!-- Use v-for to create a list of dots -->
        <div
          v-for="step in totalSteps"
          :key="step"
          :class="['dot', { active: step === currentStep, encircled: step === currentStep }]"
        ></div>
      </div>
      <div class="footer-item step d-flex flex-row justify-content-center align-items-center">
        <!-- Display the current step text -->
        <span class="current-step-text ms-2">{{ localizedText.step || 'Step' }} {{ currentStep }}/{{ totalSteps }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
// Define props received from the parent component
const props = defineProps({
  currentStep: Number,
  totalSteps: Number
})
// Reactive object to hold localized text
const localizedText = ref({
  step: ''
})

// On mounted, fetch the localized version of "Step"
onMounted(() => {
  getLocalization('Step', 'step')
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

<style scoped>
.footer {
  position: fixed;
  left: 0;
  bottom: 0;
  width: 100%;
  background-color: #f8f9fa;
  padding: 1rem 0;
  box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.1);
}

.dot {
  height: 20px; /* Increase the size for visibility */
  width: 20px; /* Increase the size for visibility */
  background-color: #bbb; /* A light grey color for dots */
  border-radius: 50%; /* Make it round */
  margin: 0 10px; /* Space out dots */
}

.dot.active {
  background-color: #007bff; /* Bootstrap primary color for active step */
}

.dot.encircled {
  border: 2px solid #007bff; /* Encircle the active step */
}

.current-step-text {
  margin-top: 1em;
  font-weight: bold;
  color: #007bff;
}

/* Ensure the dots and the text are aligned in the center */
.footer-item.step {
  display: flex; /* Use flexbox for alignment */
  align-items: center; /* Align items vertically */
  justify-content: center; /* Center items horizontally */
}
</style>
