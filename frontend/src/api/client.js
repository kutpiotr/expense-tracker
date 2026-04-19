/**
 * Thin wrapper around fetch that:
 * - Parses JSON responses automatically
 * - Throws a descriptive error for non-2xx responses
 * - Handles 204 No Content
 */
export async function request(url, options = {}) {
    const response = await fetch(url, {
        headers: {
            'Content-Type': 'application/json',
            ...(options.headers || {}),
        },
        ...options,
    })

    // 204 No Content → nothing to parse
    if (response.status === 204) {
        return null
    }

    const body = await response.json()

    if (!response.ok) {
        // API returns { error, message, details? } — we surface it as an Error
        const err = new Error(body.message || body.error || 'Request failed')
        err.status = response.status
        err.code = body.error
        err.details = body.details
        throw err
    }

    return body
}