<script setup>
defineProps({
  modelValue: [String, Number],
  label: String,
  type: {
    type: String,
    default: 'text',
  },
  placeholder: String,
  error: String,
  required: Boolean,
})

defineEmits(['update:modelValue'])
</script>

<template>
  <label class="field">
    <span v-if="label" class="field-label">
      {{ label }}
      <span v-if="required" class="field-required">*</span>
    </span>
    <input
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :class="{ 'field-input': true, 'has-error': error }"
      @input="$emit('update:modelValue', $event.target.value)"
    />
    <span v-if="error" class="field-error">{{ error }}</span>
  </label>
</template>

<style scoped>
.field {
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}

.field-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-text);
}

.field-required {
  color: var(--color-danger);
}

.field-input {
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  transition: border-color 0.15s;
}

.field-input:focus {
  outline: none;
  border-color: var(--color-primary);
}

.field-input.has-error {
  border-color: var(--color-danger);
}

.field-error {
  font-size: 0.8125rem;
  color: var(--color-danger);
}
</style>