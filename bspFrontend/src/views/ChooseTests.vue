<template>
  <div id="mainContent">
    <h1>Choose Tests</h1>
    <form @submit.prevent="handleSubmit">
      <div>
        <label for="Tests">Tests</label>
        <input type="text" id="Tests" v-model="tests.name" required />
      </div>
      <button type="submit">Select</button>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'ChooseCondition',
  setup() {
    const router = useRouter()
    const tests = ref({
      name: ''
    })

    const handleSubmit = () => {
      localStorage.setItem('tests', tests.value.name)
      router.push('/')
    }

    return { tests, handleSubmit }
  }
}
</script>

<style>
/* Add your styles here */
</style>
