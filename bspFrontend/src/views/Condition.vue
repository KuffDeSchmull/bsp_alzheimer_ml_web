<template>
  <div class="container" id="mainContent">
    <div class="row">
      <div class="col-sm-12 col-md-3"></div>
      <div class="col-sm-12 col-md-3">
        <form @submit.prevent="handleSubmit">
          <div class="mb-3">
            <label for="condition" class="form-label">{{ localizedText.condition || 'Select Condition' }}</label>
            <select class="form-select" id="condition" v-model="selectedCondition">
              <option disabled value="">{{ localizedText.selectCondition || 'Please select a condition' }}</option>
              <option value="alzheimers">{{localizedText.alzheimers || 'Alzheimer\'s'}}</option>
              <option value="parkinsons">{{localizedText.parkinsons || 'Parkinson\'s'}}</option>
            </select>
          </div>
          <button type="submit" class="btn btn-primary">{{ localizedText.submit || 'Submit' }}</button>
        </form>
      </div>
      <div class="col-sm-12 col-md-3"></div>
    </div>
    <!-- Conditionally render ChooseTest component -->
    <ChooseTest v-if="selectedCondition" :condition="selectedCondition" />
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import ChooseTest from '../components/ChooseTests.vue' // Adjust the path as necessary

export default {
  name: 'ChooseCondition',
  components: {
    ChooseTest
  },
  setup() {
    const router = useRouter()
    const selectedCondition = ref('')

    const handleSubmit = () => {
      localStorage.setItem('condition', selectedCondition.value)
      router.push('/choosetests')
    }

    return { selectedCondition, handleSubmit }
  },
  data() {
    return {
      localizedText: {
        submit: null,
        condition: null,
        selectCondition: null,
        alzheimers: null,
        parkinsons: null
        
      }
    }
  },
  mounted() {
    // Fetch initial localization for the current UI elements
    this.getLocalization('Large Font', 'largeFont')
    this.getLocalization('Serif Font', 'serifFont')
    this.getLocalization('High Contrast', 'highContrast')
    this.getLocalization('Log Out', 'logOut')
    this.getLocalization('Delete Account', 'deleteAccount')
    this.getLocalization('Choose your language', 'chooseYourLanguage')
    this.getLocalization('Choose Language', 'chooseLanguage')
    this.getLocalization('English', 'english')
    this.getLocalization('Spanish', 'spanish')
    this.getLocalization('Settings', 'settings')
  },
  methods: {
    async getLocalization(defaultText, key) {
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
          this.localizedText[key] = result.translation
        } else {
          console.error('Failed to fetch localization')
        }
      } catch (error) {
        console.error('Error fetching localization:', error)
      }
    }
  }
}
</script>

<style>
/* Add your styles here */
</style>
