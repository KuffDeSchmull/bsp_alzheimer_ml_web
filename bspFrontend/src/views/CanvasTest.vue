<script>
import VueDrawingCanvas from 'vue-drawing-canvas'
import { useTestProtocolStore } from '../stores/testProtocols'
import { useRouter } from 'vue-router'
import useTimer from '@/composables/useTimer'
import { useTestResultsStore } from '@/stores/result'
import { computed, ref } from 'vue'
import Footer from '@/components/Footer.vue'

export default {
  name: 'ServeDev',
  components: {
    VueDrawingCanvas,
    Footer
  },
  setup() {
    const testProtocolStore = useTestProtocolStore()
    const currentTask = computed(() => testProtocolStore.currentTask)
    const router = useRouter()
    const { timerDisplay, startTimer, stopTimer, resetTimer } = useTimer()
    const testIdStore = useTestResultsStore()
    const currentStep = ref(parseInt(sessionStorage.getItem('currentStep'), 10) || 1)
    const totalSteps = ref(parseInt(sessionStorage.getItem('totalSteps'), 10) || 0)
    const taskImagePath = computed(() => {
      return new URL(`../${currentTask.value.resource}`, import.meta.url).href
    })

    const handleNext = () => {
      testProtocolStore.nextStep()
      navigate()
    }

    const navigate = () => {
      if (
        parseInt(sessionStorage.getItem('currentStep'), 10) ===
        parseInt(sessionStorage.getItem('totalSteps'), 10)
      ) {
        router.push('/results')
      } else {
        router.push('/canvas')
      }
    }

    return {
      testProtocolStore,
      handleNext,
      navigate,
      timerDisplay,
      startTimer,
      stopTimer,
      resetTimer,
      testIdStore,
      currentTask,
      currentStep,
      totalSteps,
      taskImagePath
    }
  },
  data() {
    return {
      localizedText: {
        begin: '',
        start: '',
        stop: '',
        next: '', 
        done: ''
        
      },
      initialImage: [
        {
          type: 'dash',
          from: {
            x: 300,
            y: 300
          },
          coordinates: [],
          color: '#000000',
          width: 5,
          fill: false
        }
      ],
      x: 0,
      y: 0,
      image: '',
      eraser: false,
      disabled: false,
      fillShape: false,
      line: 3,
      color: '#000000',
      strokeType: 'dash',
      lineCap: 'round',
      lineJoin: 'round',
      backgroundColor: '#FFFFFF',
      backgroundImage: null,
      watermark: null,
      additionalImages: [],
      canvasLocked: true
    }
  },
  computed: {
    canvasSize() {
      const size = window.innerWidth * 1.0 // 95% of the viewport width
      return size
    }
  },
  mounted() {
    this.getLocalization('Click Start to begin the Test.', 'begin')
    this.getLocalization('Start', 'start')
    this.getLocalization('Stop', 'stop')
    this.getLocalization('Next', 'next')
    this.getLocalization('Done', 'done')
    
    if ('vue-drawing-canvas' in window.localStorage) {
      this.initialImage = JSON.parse(window.localStorage.getItem('vue-drawing-canvas'))
    }
    //this.drawClockFace();
  },
  
  methods: {
    startDrawing() {
      this.canvasLocked = false
      this.startTimer()
    },

    async finishDrawing() {
      this.stopTimer()
      console.log(`Drawing time: ${this.duration} seconds`)

      // Save the canvas image and strokes
      await this.saveCanvasImage()
      await this.saveCanvasStrokes()
      this.canvasLocked = true
    },
    async setImage(event) {
      let URL = window.URL
      this.backgroundImage = URL.createObjectURL(event.target.files[0])
      await this.$refs.VueCanvasDrawing.redraw()
    },
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
    },
    getCoordinate(event) {
      let coordinates = this.$refs.VueCanvasDrawing.getCoordinates(event)
      this.x = coordinates.x
      this.y = coordinates.y
    },
    getStrokes() {
      window.localStorage.setItem(
        'vue-drawing-canvas',
        JSON.stringify(this.$refs.VueCanvasDrawing.getAllStrokes())
      )
      alert('Strokes saved, reload your browser to see the canvas with previously saved image')
    },
    drawClockFace() {
      this.$nextTick(() => {
        const canvas = this.$refs.VueCanvasDrawing.$el
        if (canvas.getContext) {
          const ctx = canvas.getContext('2d')

          // Circle properties
          const centerX = 200
          const centerY = 200
          const radius = 200

          // Draw the circle stroke
          ctx.beginPath()
          ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI, false)
          ctx.lineWidth = 5
          ctx.strokeStyle = '#000000' // Stroke color
          ctx.stroke()
        }
      })
    },
    removeSavedStrokes() {
      window.localStorage.removeItem('vue-drawing-canvas')
      alert('Strokes cleared from local storage')
    },
    async saveCanvasImage() {
      // Get the canvas element from the VueDrawingCanvas component
      const canvasElement = this.$refs.VueCanvasDrawing.$el
      // Retrieve the session ID from sessionStorage
      const sessionId = sessionStorage.getItem('session_id')
      // Ensure that the canvas element is available
      if (canvasElement && sessionId) {
        // Convert the canvas to a data URL
        const dataURL = canvasElement.toDataURL('image/png')
        const name = sessionStorage.getItem('name')
        const surname = sessionStorage.getItem('surname')
        // Make an HTTP POST request to send the image data using the proxy URL
        try {
          const response = await fetch('/api/test/upload', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Session-ID': sessionId,
              Name: name,
              Surname: surname,
              Test: this.testProtocolStore.protocolName,
              Timer: sessionStorage.getItem('Timer')
            },
            body: JSON.stringify({ imageData: dataURL })
          })

          if (response.ok) {
            // Handle success
            const responseData = await response.json()
            this.testIdStore.addTestId(responseData.testId)
            console.log('Image sent successfully.')
            this.handleNext()
          } else {
            // Handle error
            console.error('Failed to send image.')
          }
        } catch (error) {
          // Handle network or other errors
          console.error('Error sending image:', error)
        }
      } else {
        console.error('Canvas element not found.')
      }
    },
    async saveCanvasStrokes() {
      // Get all strokes from the VueDrawingCanvas component
      const strokes = this.$refs.VueCanvasDrawing.getAllStrokes()
      // Retrieve the session ID from sessionStorage
      const sessionId = sessionStorage.getItem('session_id')
      const name = sessionStorage.getItem('name')
      const surname = sessionStorage.getItem('surname')

      // Ensure that stroke data is available
      if (strokes && strokes.length > 0 && sessionId) {
        // Make an HTTP POST request to send the stroke data using the proxy URL
        try {
          const response = await fetch('/api/test/upload-strokes', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Session-ID': sessionId,
              Name: name,
              Surname: surname
            },
            body: JSON.stringify({ strokes: strokes })
          })

          if (response.ok) {
            // Handle success
            console.log('Strokes sent successfully.')
          } else {
            // Handle error
            console.error('Failed to send strokes.')
          }
        } catch (error) {
          // Handle network or other errors
          console.error('Error sending strokes:', error)
        }
      } else {
        console.error('No strokes data found.')
      }
    }
  }
}
</script>

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
              <img
                v-if="!canvasLocked && currentTask.resource !== 'None'"
                :src="taskImagePath"
                alt="Task Image"
                class="img-fluid task-image"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="flex-row" v-if="!canvasLocked">
    <div class="source">
      <vue-drawing-canvas
        ref="VueCanvasDrawing"
        v-model:image="image"
        :width="canvasSize"
        :height="canvasSize"
        :stroke-type="strokeType"
        :line-cap="lineCap"
        :line-join="lineJoin"
        :fill-shape="fillShape"
        :eraser="eraser"
        :lineWidth="line"
        :color="color"
        :background-color="backgroundColor"
        :watermark="watermark"
        :initial-image="initialImage"
        saveAs="png"
        :styles="{
          border: 'solid 1px #000'
        }"
        :lock="canvasLocked"
        @mousemove="getCoordinate($event)"
        :additional-images="additionalImages"
      />
    </div>
  </div>
  <div class="container controls-container" id="mainContent">
    <div class="row">
      <!-- Flex container for equal height columns -->
      <div class="d-flex flex-column flex-md-row">
        <!-- Left Column for Title/Description and Buttons/Timers (Stacked on mobile, single column on desktop) -->
        <div class="d-flex flex-column col-12 col-md-6 left-col">
          <!-- Card for Buttons and Timer -->
          <div class="card mb-3 flex-fill">
            <div class="card-body">
              <span class="badge bg-secondary fs-4 timer">{{ timerDisplay }}</span>
              
              <p style="visibility: hidden">Click Start to begin the Test.</p>
              <p>{{ localizedText.begin || 'Click Start to begin the Test.' }}</p>
              <button v-if="canvasLocked" class="btn btn-primary btn-block" @click="startDrawing">
                {{ localizedText.start || 'Start' }}
              </button>
              <button v-if="!canvasLocked" class="btn btn-warning btn-block" @click="finishDrawing">
                {{ localizedText.done || 'Done' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <Footer :currentStep="currentStep" :totalSteps="totalSteps" />
</template>

<style scoped>
body {
  font-family: 'Roboto', sans-serif;
}
.flex-row {
  display: flex;
  flex-direction: row;
}
.button-container {
  display: flex;
  flex-direction: row;
}
.button-container > * {
  margin-top: 15px;
  margin-right: 10px;
}
.task-image {
  width: 45%;
  margin: auto;
}
.controls-container {
  padding-bottom: 10em;
}
</style>
