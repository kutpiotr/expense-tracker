<script setup>
import { computed } from 'vue'
import { Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from 'chart.js'
import { formatAmount } from '@/utils/format'

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps({
  data: {
    type: Array,
    required: true,
    // [{ category_name, category_color, total, percentage }]
  },
})

const chartData = computed(() => ({
  labels: props.data.map((d) => d.category_name),
  datasets: [
    {
      data: props.data.map((d) => Number(d.total)),
      backgroundColor: props.data.map((d) => d.category_color),
      borderColor: '#ffffff',
      borderWidth: 2,
    },
  ],
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: '55%',  // smaller value = thicker ring
  plugins: {
    legend: {
      position: 'right',
      labels: {
        padding: 12,
        font: { size: 13 },
      },
    },
    tooltip: {
      callbacks: {
        label(context) {
          const item = props.data[context.dataIndex]
          return `${item.category_name}: ${formatAmount(item.total)} (${item.percentage}%)`
        },
      },
    },
  },
}
</script>

<template>
  <div class="chart-container">
    <Doughnut v-if="data.length" :data="chartData" :options="chartOptions" />
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