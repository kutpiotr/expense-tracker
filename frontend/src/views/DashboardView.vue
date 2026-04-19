<script setup>
import { ref, watch, computed, onMounted } from 'vue'
import { getMonthlySummary, getByCategory, getTrend } from '@/api/stats'
import { monthBounds, formatAmount } from '@/utils/format'
import StatCard from '@/components/StatCard.vue'
import MonthSelector from '@/components/MonthSelector.vue'
import CategoryPieChart from '@/components/CategoryPieChart.vue'
import TrendLineChart from '@/components/TrendLineChart.vue'

const today = new Date()
const year = ref(today.getFullYear())
const month = ref(today.getMonth() + 1)

const summary = ref(null)
const byCategory = ref([])
const trend = ref([])

const loading = ref(false)
const error = ref(null)

const bounds = computed(() => monthBounds(year.value, month.value))

async function loadAll() {
  loading.value = true
  error.value = null
  try {
    const [summaryResult, byCategoryResult, trendResult] = await Promise.all([
      getMonthlySummary({ year: year.value, month: month.value }),
      getByCategory({ dateFrom: bounds.value.from, dateTo: bounds.value.to }),
      getTrend({ dateFrom: bounds.value.from, dateTo: bounds.value.to, granularity: 'day' }),
    ])
    summary.value = summaryResult
    byCategory.value = byCategoryResult
    trend.value = trendResult.data
  } catch (e) {
    error.value = e
  } finally {
    loading.value = false
  }
}

// Reload when month changes
watch([year, month], loadAll)

onMounted(loadAll)

const topCategory = computed(() => byCategory.value[0] || null)
</script>

<template>
  <section>
    <div class="header">
      <h2>Dashboard</h2>
      <MonthSelector v-model:year="year" v-model:month="month" />
    </div>

    <div v-if="error" class="alert-error">
      Failed to load dashboard: {{ error.message }}
    </div>

    <div v-if="loading && !summary" class="state">Loading dashboard...</div>

    <template v-else-if="summary">
      <div class="stat-grid">
        <StatCard
          label="Total spent"
          :value="formatAmount(summary.total)"
          hint="this period"
        />
        <StatCard
          label="Transactions"
          :value="summary.count"
          :hint="summary.count === 1 ? 'entry' : 'entries'"
        />
        <StatCard
          label="Average"
          :value="formatAmount(summary.average)"
          hint="per transaction"
        />
        <StatCard
          label="Active days"
          :value="summary.days_with_expenses"
          hint="with at least one expense"
        />
      </div>

      <div class="chart-grid">
        <div class="chart-panel">
          <div class="chart-header">
            <h3>By category</h3>
            <span v-if="topCategory" class="chart-subtitle">
              Top: {{ topCategory.category_name }} ({{ topCategory.percentage }}%)
            </span>
          </div>
          <CategoryPieChart :data="byCategory" />
        </div>

        <div class="chart-panel">
          <div class="chart-header">
            <h3>Daily trend</h3>
          </div>
          <TrendLineChart
            :data="trend"
            :date-from="bounds.from"
            :date-to="bounds.to"
          />
        </div>
      </div>
    </template>
  </section>
</template>

<style scoped>
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-lg);
  gap: var(--space-md);
  flex-wrap: wrap;
}

.state {
  padding: var(--space-xl);
  text-align: center;
  color: var(--color-text-muted);
}

.alert-error {
  padding: var(--space-sm) var(--space-md);
  margin-bottom: var(--space-md);
  background: #fcebeb;
  color: #791f1f;
  border: 1px solid #f7c1c1;
  border-radius: var(--radius-sm);
}

.stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: var(--space-md);
  margin-bottom: var(--space-xl);
}

.chart-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-lg);
}

@media (max-width: 900px) {
  .chart-grid {
    grid-template-columns: 1fr;
  }
}

.chart-panel {
  padding: var(--space-lg);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}

.chart-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: var(--space-md);
  gap: var(--space-md);
}

.chart-header h3 {
  font-size: 1rem;
  font-weight: 600;
}

.chart-subtitle {
  font-size: 0.875rem;
  color: var(--color-text-muted);
}
</style>