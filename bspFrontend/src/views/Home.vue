<script setup>
import { onMounted, ref, computed } from 'vue'
import TestListItem from '@/components/TestListItem.vue'
import useTestProtocols from '@/composables/useTestProtocols'
const name = sessionStorage.getItem('name')
const surname = sessionStorage.getItem('surname')
const localizedText = ref({
  greeting: '',
  availableTests: ''
})

const { testProtocols, fetchTestProtocols } = useTestProtocols()

onMounted(() => {
  fetchTestProtocols()
  // Fetch localized versions of the texts
  getLocalization('Greetings, ', 'greeting')
  getLocalization('Available Tests', 'availableTests')
  
})
const formattedDate = computed(() => {
  const today = new Date()
  return today.toLocaleDateString(undefined, {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
})
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

<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <!-- Greeting Card -->
      <div class="col-md-8 mb-4">
        <div class="card">
          <div class="card-body">
            <h2 class="card-title">{{ localizedText.greeting || 'Greetings, ' }} {{ name }} {{ surname }}!</h2>
            <p>{{ formattedDate }}</p>
          </div>
        </div>
      </div>

      <!-- Test List Card -->
      <div class="col-md-8" id="mainContent">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{{ localizedText.availableTests || 'Available Tests' }}</h5>
            <ul class="list-unstyled tests-list">
              <li v-for="test in testProtocols" :key="test.type">
                <TestListItem :test="test" />
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.tests-list {
  margin-top: 2em;
}
</style>
