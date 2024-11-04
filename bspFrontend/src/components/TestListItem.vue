<template>
  <div class="mb-3">
    <button class="btn btn-outline-primary btn-block" @click="selectTest">
      {{ test.name }}
    </button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { defineProps } from 'vue'

const props = defineProps({
  test: Object
})

const router = useRouter()

const selectTest = () => {
  router.push({
    name: 'InputMethod',
    query: {
      testName: props.test.name,
      testType: props.test.type,
      taskCount: props.test.taskCount
    }
  })
}
</script>

<style scoped>
.btn-block {
  width: 100%;
  display: block;
}
</style>
