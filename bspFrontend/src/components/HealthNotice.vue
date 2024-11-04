<template>
  <div class="card mb-3 flex-fill">
    <div class="card-body">
      <h5 class="card-title">{{ localizedText.healthNotice || 'Health Notice' }}</h5>
      <p v-for="(notice, index) in formattedNotices" :key="index" v-html="notice"></p>
    </div>
  </div>
</template>

<script setup>
import { defineProps, computed, ref, onMounted } from 'vue'

const localizedText = ref({
  healthNotice: ''
})
onMounted(() => {
  getLocalization('Health Notice', 'healthNotice')
})

const props = defineProps({
  healthNotices: {
    type: Array,
    required: true
  }
})

const formattedNotices = computed(() => {
  return props.healthNotices.slice(0, -1).map((notice) => {
    return notice.replace(/<([^>]+)>/g, (_, text) => {
      const url = props.healthNotices[props.healthNotices.length - 1]
      return `<a href="${url}" target="_blank">${text}</a>`
    })
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

<style scoped></style>
