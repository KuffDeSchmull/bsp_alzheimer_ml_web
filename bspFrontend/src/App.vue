<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
import { useAccessibilityStore } from '@/stores/settings'

const accessibilityStore = useAccessibilityStore()
</script>

<template>
  <div
    :class="{
      'large-font': accessibilityStore.useLargeFont,
      'serif-font': accessibilityStore.useSerifFont,
      'high-contrast': accessibilityStore.highContrast
    }"
  >
    <a href="#mainContent" class="skip-link sr-only" tabindex="0">Skip to main content</a>
    <Navbar />
    <RouterView />
  </div>
</template>

<style>
.skip-link.sr-only:focus {
  position: fixed;
  top: 10px;
  left: 10px;
  z-index: 1000;
  background: #f8f9fa;
  color: #212529;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  box-shadow: 0 0 3px rgba(0, 0, 0, 0.25);
  outline: none;
  text-decoration: none;
}
.skip-link {
  position: absolute;
  top: -100px;
  left: 0;
  background: #000;
  color: white;
  padding: 8px 16px;
  z-index: 100;
  transition: top 0.3s;
}

.skip-link:focus {
  top: 0;
}
.large-font {
  font-size: 2.25em;
}

.serif-font {
  font-family: 'Times New Roman', serif;
}
::v-deep .large-font h1,
::v-deep .large-font h2,
::v-deep .large-font h3,
::v-deep .large-font h4,
::v-deep .large-font h5,
::v-deep .large-font h6,
::v-deep .large-font p,
::v-deep .large-font a,
::v-deep .large-font button {
  font-size: 1.25em !important;
}
::v-deep .serif-font {
  font-family: 'Times New Roman', serif;
}
.high-contrast {
  filter: contrast(1.5); /* You can adjust the value as needed */
}
</style>
