<script setup>
import { ref, watch, computed } from 'vue'
import BaseInput from './BaseInput.vue'
import BaseSelect from './BaseSelect.vue'
import BaseButton from './BaseButton.vue'

const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
  },
  categories: {
    type: Array,
    required: true,
  },
})

const emit = defineEmits(['update:modelValue'])

const from = ref(props.modelValue.from)
const to = ref(props.modelValue.to)
const categoryId = ref(props.modelValue.categoryId)
const q = ref(props.modelValue.q)

const categoryOptions = computed(() =>
  props.categories.map((c) => ({ value: c.id, label: c.name })),
)

function emitUpdate() {
  emit('update:modelValue', {
    from: from.value,
    to: to.value,
    categoryId: categoryId.value,
    q: q.value,
  })
}

// Immediate emit for date and category filters
watch([from, to, categoryId], emitUpdate)

// Debounced emit for search text — don't hammer the API on every keystroke
let qTimer = null
watch(q, () => {
  clearTimeout(qTimer)
  qTimer = setTimeout(emitUpdate, 300)
})

function reset() {
  from.value = ''
  to.value = ''
  categoryId.value = ''
  q.value = ''
}

const hasActiveFilters = computed(
  () => !!(from.value || to.value || categoryId.value || q.value),
)
</script>

<template>
  <div class="filters">
    <BaseInput v-model="from" label="From" type="date" />
    <BaseInput v-model="to" label="To" type="date" />
    <BaseSelect
      v-model="categoryId"
      label="Category"
      :options="categoryOptions"
      placeholder="All categories"
    />
    <BaseInput v-model="q" label="Search" placeholder="Description contains..." />
    <div class="reset-wrapper">
      <BaseButton v-if="hasActiveFilters" variant="secondary" @click="reset">
        Clear
      </BaseButton>
    </div>
  </div>
</template>

<style scoped>
.filters {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: var(--space-md);
  align-items: end;
  padding: var(--space-md);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  margin-bottom: var(--space-lg);
}

.reset-wrapper {
  display: flex;
  align-items: flex-end;
}
</style>