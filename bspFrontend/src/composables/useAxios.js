// src/composables/useAxios.js
import axios from 'axios'

export default function useAxios() {
  const sessionId = sessionStorage.getItem('session_id')
  //if language in sessionStorage is null, set it to default
  if (!sessionStorage.getItem('language')) {
    sessionStorage.setItem('language', '')
  }
  const language = sessionStorage.getItem('language')

  const axiosInstance = axios.create({
    headers: {
      'Session-ID': sessionId,
      'language': language
    }
  })

  // Any other Axios configuration can go here

  return axiosInstance
}
