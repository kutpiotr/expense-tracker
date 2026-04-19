import { ref, watch } from 'vue'

/**
 * Creates a new ref that mirrors the source ref with a delay.
 * Useful for debouncing user input before triggering expensive operations.
 *
 * Usage:
 *   const search = ref('')
 *   const debouncedSearch = useDebouncedRef(search, 300)
 *   watch(debouncedSearch, (value) => { fetchResults(value) })
 */
export function useDebouncedRef(source, delay = 300) {
    const debounced = ref(source.value)
    let timer = null

    watch(source, (newValue) => {
        clearTimeout(timer)
        timer = setTimeout(() => {
            debounced.value = newValue
        }, delay)
    }, { deep: true })

    return debounced
}