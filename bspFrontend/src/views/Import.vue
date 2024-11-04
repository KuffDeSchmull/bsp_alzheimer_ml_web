<template>
  <div class="container mt-4" id="mainContent">
    <!-- Card for Drag and Drop Area and Import Button -->
    <div class="card mb-3" v-if="!imageSrc">
      <div class="card-body">
        <h5 class="card-title">Import or Take Picture</h5>
        <!-- Drag and Drop Area for Desktop -->
        <div
          class="drop-area d-none d-md-block border p-3 mb-3 text-center"
          @dragover.prevent="onDragOver"
          @drop.prevent="onDrop"
          @click="triggerFileInput"
        >
          Drag and drop an image here or click to select a file
        </div>

        <!-- File Import Button for Desktop and Mobile -->
        <input
          id="cypress-input"
          type="file"
          ref="fileInput"
          @change="onFileChange"
          accept="image/png, image/jpeg, image/heic"
          hidden
        />
        <button class="btn btn-primary" @click="triggerFileInput">Import Image</button>

        <!-- Camera Input for Mobile -->
        <input
          type="file"
          ref="cameraInput"
          @change="onFileChange"
          accept="image/*"
          capture="environment"
          hidden
        />
        <button class="btn btn-secondary" @click="triggerCameraInput">Take Picture</button>
      </div>
      <!-- Image Display -->
    </div>
    <div v-if="imageSrc" class="cropper-container mt-3">
      <img ref="img" :src="imageSrc" class="cropper-image" />
    </div>

    <div class="card mb-3 send-card" v-if="imageSrc">
      <div class="card-body">
        <button v-if="imageSrc" class="btn btn-danger mt-3" @click="clearImage">Clear Image</button>
        <button v-if="imageSrc" class="btn btn-success mt-3" @click="removeExifAndSendImage">
          Send Image
        </button>
      </div>
      <!-- Image Display -->
    </div>
  </div>
  <Footer :currentStep="currentStep" :totalSteps="totalSteps" />
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import Footer from '@/components/Footer.vue'
import EXIF from 'exif-js'
import { ref, onMounted } from 'vue'
import { useTestProtocolStore } from '@/stores/testProtocols'
import { useTestResultsStore } from '@/stores/result'
import heic2any from 'heic2any'

const route = useRoute()
const router = useRouter()
const fileInput = ref(null)
const cameraInput = ref(null)
const imageSrc = ref(null)
const testProtocolStore = useTestProtocolStore()
const currentTask = ref(testProtocolStore.currentTask)
const testIdStore = useTestResultsStore()

// Initialize step information from sessionStorage
const currentStep = ref(parseInt(sessionStorage.getItem('currentStep'), 10) || 1)
const totalSteps = ref(parseInt(sessionStorage.getItem('totalSteps'), 10) || 0)

onMounted(() => {
  // Update currentTask on component mount, in case the store has changed
  currentTask.value = testProtocolStore.currentTask
  console.log(testProtocolStore.protocolName)
})
const convertHEICToPNG = async (heicBlob) => {
  try {
    const pngBlob = await heic2any({
      blob: heicBlob,
      toType: 'image/png',
      quality: 1.0 // Quality of the output PNG
    })
    return pngBlob
  } catch (e) {
    console.error('Error converting HEIC to PNG:', e)
    throw e
  }
}
const clearImage = () => {
  imageSrc.value = null
}

const onFileChange = async (event) => {
  const files = event.target.files || event.dataTransfer.files
  if (!files.length || files.length > 1 || !files[0].type.startsWith('image/')) {
    alert('Please select a valid image file.')
    return
  }

  let file = files[0]
  if (file.type === 'image/heic') {
    try {
      file = await convertHEICToPNG(file)
    } catch (error) {
      alert('Error converting HEIC to PNG.')
      return
    }
  }

  const reader = new FileReader()
  reader.onload = (e) => {
    imageSrc.value = e.target.result
  }
  reader.readAsDataURL(file)
}

const triggerFileInput = () => fileInput.value.click()
const triggerCameraInput = () => cameraInput.value.click()
const onDragOver = (event) => event.preventDefault()
const onDrop = (event) => onFileChange(event)

//Remove EXIF data from the image
const removeExif = async (imageFile) => {
  return new Promise((resolve, reject) => {
    EXIF.getData(imageFile, function () {
      // Create canvas element to manipulate the image
      const canvas = document.createElement('canvas')
      const ctx = canvas.getContext('2d')
      const img = new Image()

      img.onload = () => {
        canvas.width = img.width
        canvas.height = img.height
        ctx.drawImage(img, 0, 0)
        resolve(canvas.toDataURL('image/png'))
      }

      img.onerror = reject

      // Convert File to a Data URL and set it as the image source
      img.src = URL.createObjectURL(imageFile)
    })
  })
}

const removeExifAndSendImage = async () => {
  const sessionId = sessionStorage.getItem('session_id')
  if (sessionId && imageSrc.value) {
    try {
      // Convert the image source to a Blob
      const processImage = await fetch(imageSrc.value)
      const imageBlob = await processImage.blob()

      // Remove EXIF data
      const cleanedDataUrl = await removeExif(imageBlob)

      // Send the cleaned image
      const name = sessionStorage.getItem('name')
      const surname = sessionStorage.getItem('surname')
      const response = await fetch('/api/test/upload', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Session-ID': sessionId,
          Name: name,
          Surname: surname,
          Test: testProtocolStore.protocolName,
          Timer: sessionStorage.getItem('Timer')
        },
        body: JSON.stringify({ imageData: cleanedDataUrl })
      })
      const responseData = await response.json()
      testIdStore.addTestId(responseData.testId)
      console.log('Image sent successfully.')
      handleNext()
    } catch (error) {
      console.error('Error in processing or sending image:', error)
    }
  } else {
    console.error('Image or session data not found.')
  }
}
const handleNext = () => {
  testProtocolStore.nextStep()
  navigate()
}
const navigate = () => {
  if (
    parseInt(sessionStorage.getItem('currentStep'), 10) ==
    parseInt(sessionStorage.getItem('totalSteps'), 10)
  ) {
    router.push('/results')
  } else {
    router.push('/draw')
  }
}
</script>

<style>
.drop-area {
  cursor: pointer;
  text-align: center;
}

.image-preview img {
  max-width: 100%;
  height: auto;
}
/* Make sure the size of the image fits perfectly into the container */
img {
  display: block;

  /* This rule is very important, please don't ignore this */
  max-width: 100%;
}
.cropper-image {
  display: block;
  max-width: 100%;
}
.card-title {
  margin-bottom: 1em;
}
.send-card {
  margin-top: 1em;
}
</style>
