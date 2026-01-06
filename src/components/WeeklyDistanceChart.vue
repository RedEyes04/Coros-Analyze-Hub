<script setup>
import { computed } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart } from 'echarts/charts'
import { 
  GridComponent, 
  TooltipComponent
} from 'echarts/components'
import VChart from 'vue-echarts'
import { useTrainingData } from '@/composables/useTrainingData'

use([
  CanvasRenderer,
  BarChart,
  GridComponent,
  TooltipComponent
])

const { aggregatedData } = useTrainingData()

// 按周聚合数据
const weeklyData = computed(() => {
  const data = aggregatedData.value
  if (!data || data.length === 0) return []
  
  // 按周分组
  const weeks = new Map()
  
  data.forEach(day => {
    const dateStr = String(day.date)
    const year = parseInt(dateStr.substring(0, 4))
    const month = parseInt(dateStr.substring(4, 6)) - 1
    const dayNum = parseInt(dateStr.substring(6, 8))
    const date = new Date(year, month, dayNum)
    
    // 获取周一的日期作为周标识
    const weekStart = new Date(date)
    const dayOfWeek = date.getDay()
    const diff = dayOfWeek === 0 ? 6 : dayOfWeek - 1
    weekStart.setDate(date.getDate() - diff)
    
    const weekKey = weekStart.toISOString().split('T')[0]
    
    if (!weeks.has(weekKey)) {
      weeks.set(weekKey, {
        weekStart,
        distance: 0,
        trainingLoad: 0,
        days: 0
      })
    }
    
    const week = weeks.get(weekKey)
    week.distance += day.distance
    week.trainingLoad += day.trainingLoad
    week.days += 1
  })
  
  // 转换为数组并排序
  return Array.from(weeks.values())
    .sort((a, b) => a.weekStart - b.weekStart)
    .slice(-12) // 最近 12 周
    .map(week => ({
      ...week,
      label: `${week.weekStart.getMonth() + 1}/${week.weekStart.getDate()}`,
      weekLabel: week.weekStart.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' }) + ' 周'
    }))
})

const chartOption = computed(() => {
  const data = weeklyData.value
  
  if (!data || data.length === 0) return {}
  
  // 计算平均周跑量
  const avgDistance = data.reduce((sum, w) => sum + w.distance, 0) / data.length
  
  return {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      backgroundColor: '#ffffff',
      borderColor: '#e8e8ed',
      borderWidth: 1,
      padding: [12, 16],
      textStyle: {
        color: '#1d1d1f',
        fontSize: 13,
        fontFamily: '-apple-system, BlinkMacSystemFont, sans-serif'
      },
      formatter: (params) => {
        const item = params[0]
        const weekData = data[item.dataIndex]
        return `
          <div style="font-weight: 600; margin-bottom: 8px;">${weekData.weekLabel}</div>
          <div style="display: flex; justify-content: space-between; gap: 20px;">
            <span style="color: #6e6e73;">周跑量</span>
            <span style="font-weight: 600; color: #0071e3;">${item.value.toFixed(1)} km</span>
          </div>
          <div style="display: flex; justify-content: space-between; gap: 20px; margin-top: 4px;">
            <span style="color: #6e6e73;">训练天数</span>
            <span style="color: #1d1d1f;">${weekData.days} 天</span>
          </div>
          <div style="display: flex; justify-content: space-between; gap: 20px; margin-top: 4px;">
            <span style="color: #6e6e73;">总负荷</span>
            <span style="color: #1d1d1f;">${weekData.trainingLoad}</span>
          </div>
        `
      },
      extraCssText: 'border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);'
    },
    grid: {
      left: 0,
      right: 0,
      bottom: 24,
      top: 20,
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: data.map(w => w.label),
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        color: '#86868b',
        fontSize: 11,
        margin: 12
      }
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        color: '#86868b',
        fontSize: 11,
        formatter: '{value}'
      },
      splitLine: {
        lineStyle: {
          color: '#f5f5f7',
          type: 'solid'
        }
      }
    },
    series: [
      {
        name: '周跑量',
        type: 'bar',
        data: data.map(w => w.distance),
        itemStyle: {
          color: '#0071e3',
          borderRadius: [6, 6, 0, 0]
        },
        barMaxWidth: 32,
        emphasis: {
          itemStyle: {
            color: '#0077ed'
          }
        },
        markLine: {
          silent: true,
          symbol: 'none',
          lineStyle: {
            color: '#ff9500',
            type: 'dashed',
            width: 1.5
          },
          data: [
            {
              yAxis: avgDistance,
              label: {
                show: true,
                position: 'end',
                formatter: `均 ${avgDistance.toFixed(0)}`,
                color: '#ff9500',
                fontSize: 11,
                fontWeight: 500
              }
            }
          ]
        }
      }
    ]
  }
})

// 统计数据
const stats = computed(() => {
  const data = weeklyData.value
  if (!data || data.length === 0) {
    return { max: 0, avg: 0, total: 0 }
  }
  
  const distances = data.map(w => w.distance)
  const max = Math.max(...distances)
  const avg = distances.reduce((a, b) => a + b, 0) / distances.length
  const total = distances.reduce((a, b) => a + b, 0)
  
  return {
    max: max.toFixed(1),
    avg: avg.toFixed(1),
    total: total.toFixed(0)
  }
})
</script>

<template>
  <div class="weekly-chart">
    <div class="chart-header">
      <div class="header-left">
        <h3 class="chart-title">周跑量趋势</h3>
        <span class="chart-subtitle">最近 12 周</span>
      </div>
      <div class="header-stats">
        <div class="mini-stat">
          <span class="mini-value">{{ stats.max }}</span>
          <span class="mini-label">最高</span>
        </div>
        <div class="mini-stat">
          <span class="mini-value">{{ stats.avg }}</span>
          <span class="mini-label">平均</span>
        </div>
      </div>
    </div>
    
    <div class="chart-wrapper">
      <v-chart 
        v-if="weeklyData.length > 0"
        :option="chartOption" 
        autoresize 
        class="echarts-instance"
      />
      <div v-else class="chart-empty">暂无数据</div>
    </div>
  </div>
</template>

<style scoped>
.weekly-chart {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--space-4);
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.chart-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
}

.chart-subtitle {
  font-size: 12px;
  color: var(--text-tertiary);
}

.header-stats {
  display: flex;
  gap: var(--space-4);
}

.mini-stat {
  text-align: right;
}

.mini-value {
  display: block;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.2;
}

.mini-label {
  font-size: 11px;
  color: var(--text-tertiary);
}

.chart-wrapper {
  flex: 1;
  min-height: 200px;
}

.echarts-instance {
  width: 100%;
  height: 100%;
  min-height: 200px;
}

.chart-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: var(--text-tertiary);
  font-size: 15px;
}
</style>
