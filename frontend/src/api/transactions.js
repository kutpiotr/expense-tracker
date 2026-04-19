import { request } from './client'

/**
 * Build query string from an object, skipping empty values.
 * Example: { from: '2026-01-01', q: '' } → '?from=2026-01-01'
 */
function buildQueryString(params) {
    const usp = new URLSearchParams()
    for (const [key, value] of Object.entries(params)) {
        if (value !== null && value !== undefined && value !== '') {
            usp.append(key, value)
        }
    }
    const qs = usp.toString()
    return qs ? `?${qs}` : ''
}

export function listTransactions(filters = {}) {
    const qs = buildQueryString({
        from: filters.from,
        to: filters.to,
        category_id: filters.categoryId,
        q: filters.q,
    })
    return request(`/api/transactions${qs}`)
}

export function createTransaction({ amount, transactionDate, description, categoryId }) {
    return request('/api/transactions', {
        method: 'POST',
        body: JSON.stringify({
            amount,
            transaction_date: transactionDate,
            description,
            category_id: categoryId,
        }),
    })
}

export function updateTransaction(id, { amount, transactionDate, description, categoryId }) {
    const payload = {}
    if (amount !== undefined) payload.amount = amount
    if (transactionDate !== undefined) payload.transaction_date = transactionDate
    if (description !== undefined) payload.description = description
    if (categoryId !== undefined) payload.category_id = categoryId

    return request(`/api/transactions/${id}`, {
        method: 'PUT',
        body: JSON.stringify(payload),
    })
}

export function deleteTransaction(id) {
    return request(`/api/transactions/${id}`, { method: 'DELETE' })
}