<template>
  <div>
    <h1>{{ localizedText.heading || 'Choose Tests for' }} {{ condition }}</h1>
    <form @submit.prevent="handleSubmit">
      <div v-for="(test, index) in availableTests" :key="index">
        <label :for="'test-' + index">{{ test.name }}</label>
        <input :id="'test-' + index" type="text" v-model="test.input" required />
      </div>
      <button type="submit">{{ localizedText.submit || 'Select' }}</button>
    </form>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'ChooseTests',
  props: {
    condition: String
  },
  setup(props) {
    const router = useRouter()
    const tests = ref([])
    const localizedText = ref({
      heading: '',
      submit: ''
    })

    // Mock array of tests for each condition
    const conditionTests = {
      alzheimers: [
        { name: 'Cognitive Assessment', input: '' },
        { name: 'MRI Scan', input: '' }
      ],
      parkinsons: [
        { name: 'Neurological Exam', input: '' },
        { name: 'Dopamine Transporter Scan', input: '' }
      ]
    }
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
      getLocalization('Choose Tests for', 'heading')
      getLocalization('Select', 'submit')
    })

    // Computed property to get available tests based on the condition
    const availableTests = computed(() => {
      return conditionTests[props.condition] || []
    })

    const handleSubmit = () => {
      localStorage.setItem('tests', JSON.stringify(tests.value))
      router.push('/')
    }
    

    tests.value = availableTests.value // Update tests array when availableTests changes

    return { tests, handleSubmit, availableTests }
  }
}
</script>

<style>
/* Add your styles here */
</style>
