import { request } from './client'

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

export function getMonthlySummary({ year, month } = {}) {
    const qs = buildQueryString({ year, month })
    return request(`/api/stats/summary${qs}`)
}

export function getByCategory({ dateFrom, dateTo } = {}) {
    const qs = buildQueryString({ date_from: dateFrom, date_to: dateTo })
    return request(`/api/stats/by-category${qs}`)
}

export function getTrend({ dateFrom, dateTo, granularity = 'day' } = {}) {
    const qs = buildQueryString({
        date_from: dateFrom,
        date_to: dateTo,
        granularity,
    })
    return request(`/api/stats/trend${qs}`)
}