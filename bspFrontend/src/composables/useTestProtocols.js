import { ref } from 'vue'
import useAxios from './useAxios.js'

export default function useTestProtocols() {
  const testProtocols = ref([])

  const fetchTestProtocols = async () => {
    const axios = useAxios()
    try {
      const response = await axios.get('/api/test/get_protocols')
      const protocolsMap = new Map()
      Object.entries(response.data).forEach(([protocolName, protocolDetails]) => {
        const testName = protocolDetails.name
        const testType = protocolDetails.type
        if (!protocolsMap.has(testName)) {
          protocolsMap.set(testName, {
            name: testName,
            type: testType,
            types: [],
            taskCount: protocolDetails.tasks.length // Set task count based on the length of tasks array
          })
        }
        const currentTest = protocolsMap.get(testName)
        protocolDetails.tasks.forEach((task) => {
          if (!currentTest.types.includes(task.type)) {
            currentTest.types.push(task.type)
          }
        })
      })
      testProtocols.value = Array.from(protocolsMap.values())
    } catch (error) {
      console.error('Error fetching test protocols:', error)
    }
  }

  return {
    testProtocols,
    fetchTestProtocols
  }
}
