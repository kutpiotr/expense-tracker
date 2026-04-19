<script setup>
import { ref, watch, computed } from 'vue'
import BaseButton from './BaseButton.vue'
import BaseInput from './BaseInput.vue'
import BaseSelect from './BaseSelect.vue'
import { todayIso } from '@/utils/format'

const props = defineProps({
  transaction: {
    type: Object,
    default: null,
  },
  categories: {
    type: Array,
    required: true,
  },
  loading: Boolean,
  fieldErrors: {
    type: Object,
    default: () => ({}),
  },
})

const emit = defineEmits(['submit', 'cancel'])

const amount = ref('')
const transactionDate = ref(todayIso())
const description = ref('')
const categoryId = ref('')

const categoryOptions = computed(() =>
  props.categories.map((c) => ({ value: c.id, label: c.name })),
)

watch(
  () => props.transaction,
  (tx) => {
    amount.value = tx?.amount || ''
    transactionDate.value = tx?.transaction_date || todayIso()
    description.value = tx?.description || ''
    categoryId.value = tx?.category_id || ''
  },
  { immediate: true },
)

function handleSubmit() {
  emit('submit', {
    amount: amount.value,
    transactionDate: transactionDate.value,
    description: description.value.trim(),
    categoryId: Number(categoryId.value) || null,
  })
}
</script>

<template>
  <form class="transaction-form" @submit.prevent="handleSubmit">
    <BaseInput
      v-model="amount"
      label="Amount"
      type="number"
      placeholder="0.00"
      :error="fieldErrors.amount"
      required
    />

    <BaseInput
      v-model="transactionDate"
      label="Date"
      type="date"
      :error="fieldErrors.transaction_date"
      required
    />

    <BaseSelect
      v-model="categoryId"
      label="Category"
      :options="categoryOptions"
      placeholder="Select a category"
      :error="fieldErrors.category_id"
      required
    />

    <BaseInput
      v-model="description"
      label="Description"
      placeholder="e.g. Lunch at work"
      :error="fieldErrors.description"
    />

    <div class="actions">
      <BaseButton type="submit" :disabled="loading">
        {{ transaction ? 'Save changes' : 'Add transaction' }}
      </BaseButton>
      <BaseButton variant="secondary" @click="$emit('cancel')">
        Cancel
      </BaseButton>
    </div>
  </form>
</template>

<style scoped>
.transaction-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.actions {
  display: flex;
  gap: var(--space-sm);
  margin-top: var(--space-sm);
}
</style>