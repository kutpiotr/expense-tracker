import { ref } from 'vue'

/**
 * Wrapper around fetch that tracks loading and error state.
 * 
 * Usage:
 *   const { data, loading, error, execute } = useApi()
 *   await execute(() => fetch('/api/categories').then(r => r.json()))
 */
export function useApi() {
    const data = ref(null)
    const loading = ref(false)
    const error = ref(null)

    async function execute(apiCall) {
        loading.value = true
        error.value = null
        try {
            data.value = await apiCall()
            return data.value
        } catch (e) {
            error.value = e
            throw e  // rzucamy dalej, żeby caller mógł zareagować (np. nie zamykać formularza)
        } finally {
            loading.value = false
        }
    }

    return { data, loading, error, execute }
}