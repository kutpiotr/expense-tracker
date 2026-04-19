<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js'
import { formatAmount, formatDate } from '@/utils/format'

ChartJS.register(
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
  Filler,
)

const props = defineProps({
  data: {
    type: Array,
    required: true,
    // [{ period: 'YYYY-MM-DD', total: '12.50', count: 1 }]
  },
  dateFrom: String,
  dateTo: String,
})

/**
 * Fill missing days with zero values so the line is continuous.
 */
const filledData = computed(() => {
  if (!props.dateFrom || !props.dateTo) return props.data

  const byDate = Object.fromEntries(props.data.map((d) => [d.period, d]))
  const result = []
  const [fy, fm, fd] = props.dateFrom.split('-').map(Number)
  const [ty, tm, td] = props.dateTo.split('-').map(Number)
  const cursor = new Date(fy, fm - 1, fd)
  const end = new Date(ty, tm - 1, td)

  while (cursor <= end) {
    const y = cursor.getFullYear()
    const m = String(cursor.getMonth() + 1).padStart(2, '0')
    const d = String(cursor.getDate()).padStart(2, '0')
    const iso = `${y}-${m}-${d}`
    result.push(byDate[iso] || { period: iso, total: '0', count: 0 })
    cursor.setDate(cursor.getDate() + 1)
  }
  return result
})

const chartData = computed(() => ({
  labels: filledData.value.map((d) => d.period),
  datasets: [
    {
      label: 'Daily expenses',
      data: filledData.value.map((d) => Number(d.total)),
      borderColor: '#378ADD',
      backgroundColor: 'rgba(55, 138, 221, 0.15)',
      fill: true,
      tension: 0.25,
      pointRadius: 3,
      pointHoverRadius: 5,
    },
  ],
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        title(items) {
          return formatDate(items[0].label)
        },
        label(context) {
          const value = context.parsed.y
          return `${formatAmount(value)}`
        },
      },
    },
  },
  scales: {
    x: {
      ticks: {
        callback(value, index) {
          // Show day number only, not full date — keeps axis readable
          const label = this.getLabelForValue(value)
          const day = label.split('-')[2]
          // Show every 3rd day to reduce clutter
          return index % 3 === 0 ? day : ''
        },
      },
      grid: { display: false },
    },
    y: {
      beginAtZero: true,
      ticks: {
        callback(value) {
          return formatAmount(value)
        },
      },
    },
  },
}
</script>

<template>
  <div class="chart-container">
    <Line v-if="filledData.length" :data="chartData" :options="chartOptions" />
    <p v-else class="empty">No data for this period</p>
  </div>
</template>

<style scoped>
.chart-container {
  position: relative;
  height: 280px;
}

.empty {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-muted);
}
</style>