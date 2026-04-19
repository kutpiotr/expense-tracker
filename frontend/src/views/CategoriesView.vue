<script setup>
import { ref, onMounted } from 'vue'
import { listCategories, createCategory, updateCategory, deleteCategory } from '@/api/categories'
import { useApi } from '@/composables/useApi'
import BaseButton from '@/components/BaseButton.vue'
import CategoryForm from '@/components/CategoryForm.vue'

// Main list state
const categories = ref([])
const { loading: listLoading, error: listError, execute: executeList } = useApi()

// Form state
const editingCategory = ref(null)  // null when creating, an object when editing
const formLoading = ref(false)
const fieldErrors = ref({})

// Feedback to the user
const message = ref(null)  // { text, type: 'success' | 'error' }

async function loadCategories() {
  try {
    categories.value = await executeList(listCategories)
  } catch (e) {
    console.error('Failed to load categories:', e)
  }
}

function startEdit(category) {
  editingCategory.value = { ...category }
  fieldErrors.value = {}
  // Scroll to form — small UX touch
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function cancelEdit() {
  editingCategory.value = null
  fieldErrors.value = {}
}

async function handleSubmit(payload) {
  formLoading.value = true
  fieldErrors.value = {}
  try {
    if (editingCategory.value) {
      await updateCategory(editingCategory.value.id, payload)
      showMessage('Category updated', 'success')
    } else {
      await createCategory(payload)
      showMessage('Category added', 'success')
    }
    editingCategory.value = null
    await loadCategories()
  } catch (e) {
    handleError(e)
  } finally {
    formLoading.value = false
  }
}

async function handleDelete(category) {
  const confirmed = window.confirm(
    `Delete category "${category.name}"? All its transactions will be deleted too.`,
  )
  if (!confirmed) return

  try {
    await deleteCategory(category.id)
    showMessage(`Category "${category.name}" deleted`, 'success')
    await loadCategories()
  } catch (e) {
    showMessage(e.message, 'error')
  }
}

function handleError(e) {
  if (e.code === 'validation_error' && e.details) {
    // Extract per-field errors from the backend response
    const errors = {}
    for (const detail of e.details) {
      errors[detail.field] = detail.message
    }
    fieldErrors.value = errors
  } else if (e.code === 'integrity_error') {
    showMessage('A category with this name already exists', 'error')
  } else {
    showMessage(e.message || 'Something went wrong', 'error')
  }
}

function showMessage(text, type) {
  message.value = { text, type }
  setTimeout(() => {
    message.value = null
  }, 3500)
}

onMounted(loadCategories)
</script>

<template>
  <section>
    <h2>Categories</h2>

    <div v-if="message" :class="['alert', `alert-${message.type}`]">
      {{ message.text }}
    </div>

    <CategoryForm
      :category="editingCategory"
      :loading="formLoading"
      :field-errors="fieldErrors"
      @submit="handleSubmit"
      @cancel="cancelEdit"
    />

    <div class="list-wrapper">
      <p v-if="listLoading" class="state">Loading...</p>

      <p v-else-if="listError" class="state error">
        Failed to load categories: {{ listError.message }}
      </p>

      <p v-else-if="categories.length === 0" class="state">
        No categories yet. Add your first one above.
      </p>

      <ul v-else class="category-list">
        <li v-for="category in categories" :key="category.id" class="category-item">
          <span class="category-swatch" :style="{ background: category.color }" />
          <span class="category-name">{{ category.name }}</span>
          <span class="category-actions">
            <BaseButton variant="secondary" @click="startEdit(category)">Edit</BaseButton>
            <BaseButton variant="danger" @click="handleDelete(category)">Delete</BaseButton>
          </span>
        </li>
      </ul>
    </div>
  </section>
</template>

<style scoped>
h2 {
  margin-bottom: var(--space-lg);
}

.alert {
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius-sm);
  margin-bottom: var(--space-md);
}

.alert-success {
  background: #e3f4ec;
  color: #0f6e56;
  border: 1px solid #9fe1cb;
}

.alert-error {
  background: #fcebeb;
  color: #791f1f;
  border: 1px solid #f7c1c1;
}

.list-wrapper {
  margin-top: var(--space-xl);
}

.state {
  color: var(--color-text-muted);
  padding: var(--space-md);
}

.state.error {
  color: var(--color-danger);
}

.category-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.category-item {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-md);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}

.category-swatch {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  flex-shrink: 0;
  border: 1px solid var(--color-border);
}

.category-name {
  flex: 1;
  font-weight: 500;
}

.category-actions {
  display: flex;
  gap: var(--space-sm);
}
</style>