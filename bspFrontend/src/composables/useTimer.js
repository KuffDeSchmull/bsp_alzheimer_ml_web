import { ref } from 'vue'

export default function useTimer() {
  const timerDisplay = ref('00:00')
  let interval = null
  let elapsedSeconds = ref(0)

  const saveTime = (time) => {
    sessionStorage.setItem('Timer', time.toString())
  }

  const startTimer = () => {
    elapsedSeconds.value = 0
    interval = setInterval(() => {
      elapsedSeconds.value++
      timerDisplay.value = new Date(elapsedSeconds.value * 1000).toISOString().substr(14, 5)
    }, 1000)
  }

  const stopTimer = () => {
    clearInterval(interval)
    saveTime(elapsedSeconds.value)
    return elapsedSeconds.value // Return the elapsed time in seconds
  }

  const resetTimer = () => {
    clearInterval(interval)
    elapsedSeconds.value = 0
    timerDisplay.value = '00:00'
  }

  return { timerDisplay, startTimer, stopTimer, resetTimer }
}
