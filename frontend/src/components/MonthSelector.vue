<script setup>
import { computed } from 'vue'
import { formatMonth } from '@/utils/format'

const props = defineProps({
  year: { type: Number, required: true },
  month: { type: Number, required: true },
})

const emit = defineEmits(['update:year', 'update:month'])

const label = computed(() => formatMonth(props.year, props.month))

function shift(direction) {
  let newMonth = props.month + direction
  let newYear = props.year
  if (newMonth < 1) {
    newMonth = 12
    newYear -= 1
  } else if (newMonth > 12) {
    newMonth = 1
    newYear += 1
  }
  emit('update:year', newYear)
  emit('update:month', newMonth)
}

// Disable "next" when already on current or future month
const now = new Date()
const isCurrentOrFuture = computed(
  () => props.year > now.getFullYear() ||
        (props.year === now.getFullYear() && props.month >= now.getMonth() + 1),
)
</script>

<template>
  <div class="month-selector">
    <button type="button" class="arrow" @click="shift(-1)" aria-label="Previous month">‹</button>
    <span class="label">{{ label }}</span>
    <button
      type="button"
      class="arrow"
      :disabled="isCurrentOrFuture"
      @click="shift(1)"
      aria-label="Next month"
    >›</button>
  </div>
</template>

<style scoped>
.month-selector {
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-xs) var(--space-sm);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}

.arrow {
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  border-radius: var(--radius-sm);
  font-size: 1.25rem;
  line-height: 1;
  color: var(--color-text);
}

.arrow:hover:not(:disabled) {
  background: var(--color-bg);
}

.arrow:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.label {
  min-width: 140px;
  text-align: center;
  font-weight: 500;
}
</style>