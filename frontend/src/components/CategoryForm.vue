<script setup>
import { ref, watch } from 'vue'
import BaseButton from './BaseButton.vue'
import BaseInput from './BaseInput.vue'

const props = defineProps({
  // If provided, form is in edit mode; otherwise creating a new category
  category: {
    type: Object,
    default: null,
  },
  loading: Boolean,
  // Server-side field errors: { name: '...', color: '...' }
  fieldErrors: {
    type: Object,
    default: () => ({}),
  },
})

const emit = defineEmits(['submit', 'cancel'])

const name = ref('')
const color = ref('#888888')

// When switching which category is being edited, refresh the form values.
watch(
  () => props.category,
  (newCategory) => {
    name.value = newCategory?.name || ''
    color.value = newCategory?.color || '#888888'
  },
  { immediate: true },
)

function handleSubmit() {
  emit('submit', { name: name.value.trim(), color: color.value })
}
</script>

<template>
  <form class="category-form" @submit.prevent="handleSubmit">
    <BaseInput
      v-model="name"
      label="Name"
      placeholder="e.g. Food"
      :error="fieldErrors.name"
      required
    />

    <label class="color-field">
      <span class="color-label">Color</span>
      <div class="color-row">
        <input v-model="color" type="color" class="color-picker" />
        <BaseInput v-model="color" type="text" placeholder="#RRGGBB" :error="fieldErrors.color" />
      </div>
    </label>

    <div class="actions">
      <BaseButton type="submit" :disabled="loading">
        {{ category ? 'Save changes' : 'Add category' }}
      </BaseButton>
      <BaseButton v-if="category" variant="secondary" @click="$emit('cancel')">
        Cancel
      </BaseButton>
    </div>
  </form>
</template>

<style scoped>
.category-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
  padding: var(--space-lg);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}

.color-field {
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}

.color-label {
  font-size: 0.875rem;
  font-weight: 500;
}

.color-row {
  display: flex;
  gap: var(--space-sm);
  align-items: flex-start;
}

.color-picker {
  width: 48px;
  height: 38px;
  padding: 2px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  cursor: pointer;
  background: var(--color-surface);
}

.actions {
  display: flex;
  gap: var(--space-sm);
}
</style>