/**
 * Format a decimal amount as a display string with 2 decimal places.
 * Input: "12.5" or 12.5 → "12.50"
 */
export function formatAmount(value) {
    const num = Number(value)
    if (Number.isNaN(num)) return '0.00'
    return num.toFixed(2)
}

/**
 * Format an ISO date string "YYYY-MM-DD" in the user's locale.
 * Parses manually to avoid UTC/timezone issues.
 */
export function formatDate(isoDate) {
    if (!isoDate) return ''
    const [year, month, day] = isoDate.split('-').map(Number)
    const date = new Date(year, month - 1, day)
    return date.toLocaleDateString(undefined, {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
    })
}

/**
 * Return today's date as "YYYY-MM-DD" using local time.
 */
export function todayIso() {
    const now = new Date()
    const year = now.getFullYear()
    const month = String(now.getMonth() + 1).padStart(2, '0')
    const day = String(now.getDate()).padStart(2, '0')
    return `${year}-${month}-${day}`
}
