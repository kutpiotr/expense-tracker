<script setup>
defineProps({
  modelValue: [String, Number, null],
  label: String,
  options: {
    type: Array,
    required: true,
    // Each option: { value, label }
  },
  placeholder: {
    type: String,
    default: 'Select...',
  },
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
    <select
      :value="modelValue"
      :class="{ 'field-select': true, 'has-error': error }"
      @change="$emit('update:modelValue', $event.target.value)"
    >
      <option value="">{{ placeholder }}</option>
      <option v-for="option in options" :key="option.value" :value="option.value">
        {{ option.label }}
      </option>
    </select>
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
}

.field-required {
  color: var(--color-danger);
}

.field-select {
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  font-size: inherit;
  cursor: pointer;
}

.field-select:focus {
  outline: none;
  border-color: var(--color-primary);
}

.field-select.has-error {
  border-color: var(--color-danger);
}

.field-error {
  font-size: 0.8125rem;
  color: var(--color-danger);
}
</style>