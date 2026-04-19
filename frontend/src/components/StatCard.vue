<script setup>
defineProps({
  label: String,
  value: [String, Number],
  hint: String,  // optional subtitle, e.g. "this month"
})
</script>

<template>
  <div class="stat-card">
    <div class="stat-label">{{ label }}</div>
    <div class="stat-value">{{ value }}</div>
    <div v-if="hint" class="stat-hint">{{ hint }}</div>
  </div>
</template>

<style scoped>
.stat-card {
  padding: var(--space-lg);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}

.stat-label {
  font-size: 0.8125rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-text-muted);
  margin-bottom: var(--space-sm);
}

.stat-value {
  font-size: 2rem;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  line-height: 1.1;
}

.stat-hint {
  margin-top: var(--space-xs);
  font-size: 0.875rem;
  color: var(--color-text-muted);
}
</style>