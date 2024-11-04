<template>
  <div class="container">
    <div class="row">
      <!-- Flex container for equal height columns -->
      <div class="d-flex flex-column flex-md-row">
        <!-- Left Column for Title/Description and Buttons/Timers (Stacked on mobile, single column on desktop) -->
        <div class="d-flex flex-column col-12 col-md-6 left-col">
          <!-- Card for Title and Description -->
          <div class="card mb-3 flex-fill">
            <div class="card-body">
              <h5 class="card-title">{{ currentTask.name }}</h5>
              <p>{{ currentTask.instruction }}</p>
            </div>
          </div>

          <!-- Card for Buttons and Timer -->
          <div class="card mb-3 flex-fill" id="mainContent">
            <div class="card-body">
              <span class="badge bg-secondary fs-4 timer">{{ timerDisplay }}</span>
              <p style="visibility: hidden;">Click Start to begin the Test.</p>
              <p>{{ localizedText.begin || 'Click Start to begin the Test.' }}</p>
              <button v-if="!isTimerStarted" class="btn btn-primary btn-block" @click="start">
                {{ localizedText.start || 'Start' }}
              </button>
              <button v-if="isTimerRunning" class="btn btn-warning btn-block" @click="stop">
                {{ localizedText.stop || 'Stop' }}
              </button>
              <button v-if="isTimerStopped" class="btn btn-success btn-block" @click="goToNext">
                {{ localizedText.next || 'Next' }}
              </button>
            </div>
          </div>
        </div>

        <!-- Right Column for Image (Full width on mobile, right column on desktop) -->
        <div
          class="image-card d-flex flex-column col-12 col-md-6"
          v-if="isTimerStarted && currentTask.resource !== 'None'"
        >
          <!-- Card for Image -->
          <div class="card mb-3">
            <div class="card-body text-center d-flex align-items-center justify-content-center">
              <img :src="taskImagePath" alt="Task Image" class="img-fluid task-image" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <Footer :currentStep="currentStep" :totalSteps="totalSteps" />
</template>

<script setup>
import Footer from '@/components/Footer.vue'
import { ref, computed , onMounted} from 'vue'
import { useTestProtocolStore } from '@/stores/testProtocols'
import { useRouter } from 'vue-router'
import useTimer from '@/composables/useTimer'

const localizedText = ref({
  begin: '',
  start: '',
  stop: '',
  next: ''
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

onMounted(() => {
  getLocalization('Click Start to begin the Test.', 'begin')
  getLocalization('Start', 'start')
  getLocalization('Stop', 'stop')
  getLocalization('Next', 'next')
  
})

const { timerDisplay, startTimer, stopTimer, resetTimer } = useTimer()
const router = useRouter()
const testProtocolStore = useTestProtocolStore()

const currentTask = computed(() => testProtocolStore.currentTask)
const currentStep = ref(parseInt(sessionStorage.getItem('currentStep'), 10) || 1)
const totalSteps = ref(parseInt(sessionStorage.getItem('totalSteps'), 10) || 0)

let interval = null
const isTimerStarted = ref(false)
const isTimerRunning = ref(false)
const isTimerStopped = ref(false)


const taskImagePath = computed(() => {
  return new URL(`../${currentTask.value.resource}`, import.meta.url).href
})

const start = () => {
  isTimerStarted.value = true
  isTimerRunning.value = true
  startTimer()
}
const stop = () => {
  isTimerRunning.value = false
  isTimerStopped.value = true
  stopTimer()
}

const goToNext = () => {
  testProtocolStore.nextStep()
  router.push('/import')
}


</script>

<style scoped>
/* Add your existing styles here */

.task-image {
  max-height: 50vh; /* Limit the height to 50% of the viewport height */
  max-width: 50vw; /* Limit the width to 50% of the viewport width */
}
.no-padding {
  padding: 0;
}
.left-col {
  margin-right: 1em;
}
.timer {
  margin-bottom: 1em;
}
/* Rest of your styles */
</style>
