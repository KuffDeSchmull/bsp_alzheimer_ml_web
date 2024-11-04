<script setup>
// We may want to change this view and instead add it as a card to the previous screen, might be confusing, but else both screens feel kinda empty
import { useRoute, useRouter } from 'vue-router'
import Footer from '@/components/Footer.vue'
import { ref, computed, onMounted } from 'vue'
import useAxios from '@/composables/useAxios.js'
import { useTestProtocolStore } from '@/stores/testProtocols'

const route = useRoute()
const router = useRouter()
const testProtocolStore = useTestProtocolStore()

// Initialize refs
const selectedInputMethod = ref('')
const currentStep = ref(1)
const totalSteps = ref(3) // Default value, will be updated

const testName = computed(() => route.query.testName)
const testType = computed(() => route.query.testType)
const taskCount = computed(() => parseInt(route.query.taskCount, 10))

const localizedText = ref({
  inputMethod: '',
  paper: '',
  digital: '',
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
  getLocalization('Select Input Method', 'inputMethod')
  getLocalization('Paper Drawing', 'paper')
  getLocalization('Digital Canvas', 'digital')
  
})

// Function to calculate total steps based on test type and input method
const calculateTotalSteps = () => {
  // Base steps for every test: 1 for input method selection, 1 for result display
  let baseSteps = 2

  if (selectedInputMethod.value === 'rnn') {
    // For RNN, just the task steps and base steps
    totalSteps.value = taskCount.value + baseSteps
  } else {
    // Additional steps for CNN: 1 for importing drawing
    totalSteps.value = 2 * taskCount.value + baseSteps
  }
}

// Function to handle input method selection
const selectInputMethod = async (method) => {
  selectedInputMethod.value = method
  calculateTotalSteps()
  sessionStorage.setItem('currentStep', currentStep.value)
  sessionStorage.setItem('totalSteps', totalSteps.value)
  const axios = useAxios()
  try {
    const protocolResponse = await axios.get(`/api/test/protocol/${testType.value}/${method}`)
    console.log('Fetched protocol:', protocolResponse.data)
    testProtocolStore.setProtocol(protocolResponse.data)

    sessionStorage.setItem('currentStep', parseInt(sessionStorage.getItem('currentStep')) + 1)
    //testProtocolStore.nextStep();
    if (method === 'cnn') {
      router.push('/draw')
    } else if (method === 'rnn') {
      router.push('/canvas')
    }
    // Store the protocol data as needed and navigate to the next step
    // router.push({ name: 'NextStep' });
  } catch (error) {
    console.error('Error fetching test protocol:', error)
  }
}

// Pinia Store
</script>
<template>
  <div class="container" id="mainContent">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{{ localizedText.inputMethod || 'Select Input Method' }}</h5>
            <div class="d-grid">
              <div class="mb-3">
                <button class="btn btn-outline-primary btn-block" @click="selectInputMethod('cnn')">
                  {{ localizedText.paper || 'Paper Drawing' }}
                </button>
              </div>
              <div class="mb-3">
                <button class="btn btn-outline-primary btn-block" @click="selectInputMethod('rnn')">
                  {{ localizedText.digital || 'Digital Canvas' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <Footer :currentStep="currentStep" :totalSteps="totalSteps" />
  </div>
</template>

<style>
.container {
  margin-top: 5vh;
}
.d-grid {
  margin-top: 2em;
}
.btn-block {
  width: 100%;
  display: block;
}
</style>
