<script setup>
defineProps({
  variant: {
    type: String,
    default: 'primary',  // 'primary' | 'secondary' | 'danger'
  },
  disabled: Boolean,
  type: {
    type: String,
    default: 'button',
  },
})
</script>

<template>
  <button :type="type" :disabled="disabled" :class="['btn', `btn-${variant}`]">
    <slot />
  </button>
</template>

<style scoped>
.btn {
  padding: 0.5rem 1rem;
  border: 1px solid transparent;
  border-radius: var(--radius-sm);
  font-weight: 500;
  transition: background-color 0.15s, border-color 0.15s;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background: var(--color-primary);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: var(--color-primary-hover);
}

.btn-secondary {
  background: var(--color-surface);
  color: var(--color-text);
  border-color: var(--color-border);
}

.btn-secondary:hover:not(:disabled) {
  background: var(--color-bg);
}

.btn-danger {
  background: var(--color-danger);
  color: white;
}

.btn-danger:hover:not(:disabled) {
  filter: brightness(0.9);
}
</style>
