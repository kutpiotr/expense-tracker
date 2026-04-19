<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { listTransactions, createTransaction, updateTransaction, deleteTransaction } from '@/api/transactions'
import { listCategories } from '@/api/categories'
import BaseButton from '@/components/BaseButton.vue'
import BaseModal from '@/components/BaseModal.vue'
import TransactionForm from '@/components/TransactionForm.vue'
import TransactionFilters from '@/components/TransactionFilters.vue'
import { formatAmount, formatDate } from '@/utils/format'

const transactions = ref([])
const categories = ref([])

const listLoading = ref(false)
const listError = ref(null)

const showForm = ref(false)
const editingTransaction = ref(null)
const formLoading = ref(false)
const fieldErrors = ref({})

const filters = ref({ from: '', to: '', categoryId: '', q: '' })

const message = ref(null)

// --- Totals shown above the list -----------------------------------------
const totalsDisplay = computed(() => {
  const count = transactions.value.length
  const sum = transactions.value.reduce((acc, t) => acc + Number(t.amount), 0)
  return { count, sum: sum.toFixed(2) }
})

// --- Data loading --------------------------------------------------------
async function loadCategories() {
  try {
    categories.value = await listCategories()
  } catch (e) {
    console.error('Failed to load categories:', e)
  }
}

async function loadTransactions() {
  listLoading.value = true
  listError.value = null
  try {
    transactions.value = await listTransactions(filters.value)
  } catch (e) {
    listError.value = e
  } finally {
    listLoading.value = false
  }
}

watch(filters, loadTransactions, { deep: true })

onMounted(async () => {
  await loadCategories()
  await loadTransactions()
})

// --- Form actions --------------------------------------------------------
function openCreateForm() {
  editingTransaction.value = null
  fieldErrors.value = {}
  showForm.value = true
}

function openEditForm(transaction) {
  editingTransaction.value = { ...transaction }
  fieldErrors.value = {}
  showForm.value = true
}

function closeForm() {
  showForm.value = false
  editingTransaction.value = null
  fieldErrors.value = {}
}

async function handleSubmit(payload) {
  formLoading.value = true
  fieldErrors.value = {}
  try {
    if (editingTransaction.value) {
      await updateTransaction(editingTransaction.value.id, payload)
      showMessage('Transaction updated', 'success')
    } else {
      await createTransaction(payload)
      showMessage('Transaction added', 'success')
    }
    closeForm()
    await loadTransactions()
  } catch (e) {
    handleError(e)
  } finally {
    formLoading.value = false
  }
}

async function handleDelete(transaction) {
  const confirmed = window.confirm(
    `Delete this transaction? (${formatAmount(transaction.amount)}, ${transaction.description || 'no description'})`,
  )
  if (!confirmed) return

  try {
    await deleteTransaction(transaction.id)
    showMessage('Transaction deleted', 'success')
    await loadTransactions()
  } catch (e) {
    showMessage(e.message, 'error')
  }
}

function handleError(e) {
  if (e.code === 'validation_error' && e.details) {
    const errors = {}
    for (const detail of e.details) {
      errors[detail.field] = detail.message
    }
    fieldErrors.value = errors
  } else if (e.code === 'invalid_reference') {
    showMessage(e.message, 'error')
  } else {
    showMessage(e.message || 'Something went wrong', 'error')
  }
}

function showMessage(text, type) {
  message.value = { text, type }
  setTimeout(() => { message.value = null }, 3500)
}
</script>

<template>
  <section>
    <div class="header">
      <h2>Transactions</h2>
      <BaseButton @click="openCreateForm">+ Add transaction</BaseButton>
    </div>

    <div v-if="message" :class="['alert', `alert-${message.type}`]">
      {{ message.text }}
    </div>

    <TransactionFilters v-model="filters" :categories="categories" />

    <div class="totals">
      <span>{{ totalsDisplay.count }} transactions</span>
      <span class="totals-sum">Total: {{ totalsDisplay.sum }}</span>
    </div>

    <div class="list-wrapper">
      <p v-if="listLoading" class="state">Loading...</p>

      <p v-else-if="listError" class="state error">
        Failed to load transactions: {{ listError.message }}
      </p>

      <p v-else-if="transactions.length === 0" class="state">
        No transactions match your filters.
      </p>

      <table v-else class="transaction-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Category</th>
            <th>Description</th>
            <th class="col-amount">Amount</th>
            <th class="col-actions"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in transactions" :key="t.id">
            <td>{{ formatDate(t.transaction_date) }}</td>
            <td>
              <span v-if="t.category" class="category-badge">
                <span class="category-dot" :style="{ background: t.category.color }" />
                {{ t.category.name }}
              </span>
            </td>
            <td>{{ t.description || '—' }}</td>
            <td class="col-amount">{{ formatAmount(t.amount) }}</td>
            <td class="col-actions">
              <BaseButton variant="secondary" @click="openEditForm(t)">Edit</BaseButton>
              <BaseButton variant="danger" @click="handleDelete(t)">Delete</BaseButton>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <BaseModal
      v-model="showForm"
      :title="editingTransaction ? 'Edit transaction' : 'New transaction'"
    >
      <TransactionForm
        :transaction="editingTransaction"
        :categories="categories"
        :loading="formLoading"
        :field-errors="fieldErrors"
        @submit="handleSubmit"
        @cancel="closeForm"
      />
    </BaseModal>
  </section>
</template>

<style scoped>
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
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

.totals {
  display: flex;
  justify-content: space-between;
  margin-bottom: var(--space-md);
  color: var(--color-text-muted);
  font-size: 0.9375rem;
}

.totals-sum {
  font-weight: 600;
  color: var(--color-text);
}

.state {
  padding: var(--space-xl);
  text-align: center;
  color: var(--color-text-muted);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}

.state.error {
  color: var(--color-danger);
}

.transaction-table {
  width: 100%;
  border-collapse: collapse;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.transaction-table th {
  text-align: left;
  font-weight: 500;
  padding: var(--space-sm) var(--space-md);
  background: var(--color-bg);
  color: var(--color-text-muted);
  font-size: 0.875rem;
  border-bottom: 1px solid var(--color-border);
}

.transaction-table td {
  padding: var(--space-md);
  border-bottom: 1px solid var(--color-border);
}

.transaction-table tbody tr:last-child td {
  border-bottom: none;
}

.transaction-table tbody tr:hover {
  background: var(--color-bg);
}

.col-amount {
  text-align: right;
  font-variant-numeric: tabular-nums;
  font-weight: 500;
}

.col-actions {
  text-align: right;
  white-space: nowrap;
}

.col-actions .btn {
  margin-left: var(--space-xs);
}

.category-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-xs);
  font-size: 0.9375rem;
}

.category-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 1px solid var(--color-border);
  flex-shrink: 0;
}
</style>