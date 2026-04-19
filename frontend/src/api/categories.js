import { request } from './client'

export function listCategories() {
    return request('/api/categories')
}

export function createCategory({ name, color }) {
    return request('/api/categories', {
        method: 'POST',
        body: JSON.stringify({ name, color }),
    })
}

export function updateCategory(id, { name, color }) {
    // Build payload dynamically — only include fields that are defined.
    // Backend treats missing fields as "leave unchanged".
    const payload = {}
    if (name !== undefined) payload.name = name
    if (color !== undefined) payload.color = color

    return request(`/api/categories/${id}`, {
        method: 'PUT',
        body: JSON.stringify(payload),
    })
}

export function deleteCategory(id) {
    return request(`/api/categories/${id}`, {
        method: 'DELETE',
    })
}