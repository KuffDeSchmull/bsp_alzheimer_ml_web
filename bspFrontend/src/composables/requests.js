// composables/useBackend.js
import { useProfileStore } from '@/stores/profile'
import axios from 'axios'

export function request() {
  const profileStore = useProfileStore()
  if (!sessionStorage.getItem('language')) {
    sessionStorage.setItem('language', '')
  }
  const language = sessionStorage.getItem('language')

  const fetchResults = async () => {
    try {
      const response = await axios.get('https://your-api-domain.com/api/results', {
        headers: {
          'Session-ID': profileStore.sessionID, // Send sessionID from profile store,
          'language': language
        }
      })
      return response.data
    } catch (error) {
      console.error('Error fetching results:', error)
      throw error
    }
  }

  const saveCanvas = async (canvasData) => {
    try {
      const response = await axios.post('https://your-api-domain.com/api/saveCanvas', canvasData, {
        headers: {
          'Session-ID': profileStore.sessionID, // Ensure to send sessionID
          'language': language
        }
      })
      return response.data
    } catch (error) {
      console.error('Error saving canvas:', error)
      throw error
    }
  }

  return {
    fetchResults,
    saveCanvas
  }
}
