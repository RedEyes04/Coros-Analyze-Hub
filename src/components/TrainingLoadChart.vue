<script setup>
import { computed } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, BarChart } from 'echarts/charts'
import { 
  GridComponent, 
  TooltipComponent,
  DataZoomComponent 
} from 'echarts/components'
import VChart from 'vue-echarts'
import { useTrainingData } from '@/composables/useTrainingData'

use([
  CanvasRenderer,
  LineChart,
  BarChart,
  GridComponent,
  TooltipComponent,
  DataZoomComponent
])

const { aggregatedData, isLoading } = useTrainingData()

const chartOption = computed(() => {
  const data = aggregatedData.value
  
  if (!data || data.length === 0) {
    return {}
  }
  
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
        const dataItem = data[item.dataIndex]
        return `
          <div style="font-weight: 600; margin-bottom: 8px;">${dataItem.dateFull}</div>
          <div style="display: flex; justify-content: space-between; gap: 24px; color: #6e6e73;">
            <span>训练负荷</span>
            <span style="font-weight: 600; color: #1d1d1f;">${item.value}</span>
          </div>
        `
      },
      extraCssText: 'border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);'
    },
    grid: {
      left: 0,
      right: 0,
      bottom: 40,
      top: 20,
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: data.map(d => d.dateFormatted),
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
        fontSize: 11
      },
      splitLine: {
        lineStyle: {
          color: '#f5f5f7',
          type: 'solid'
        }
      }
    },
    dataZoom: [
      {
        type: 'inside',
        start: 50,
        end: 100
      }
    ],
    series: [
      {
        name: '训练负荷',
        type: 'bar',
        data: data.map(d => d.trainingLoad),
        itemStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: '#ff9500' },
              { offset: 1, color: '#ffcc00' }
            ]
          },
          borderRadius: [4, 4, 0, 0]
        },
        barMaxWidth: 24,
        emphasis: {
          itemStyle: {
            color: {
              type: 'linear',
              x: 0, y: 0, x2: 0, y2: 1,
              colorStops: [
                { offset: 0, color: '#ff9500' },
                { offset: 1, color: '#ffb340' }
              ]
            }
          }
        }
      }
    ]
  }
})
</script>

<template>
  <div class="chart-container">
    <div class="chart-header">
      <h3 class="chart-title">训练负荷</h3>
      <span class="chart-hint">拖动查看更多</span>
    </div>
    
    <div class="chart-wrapper">
      <v-chart 
        v-if="aggregatedData.length > 0"
        :option="chartOption" 
        autoresize 
        class="echarts-instance"
      />
      <div v-else class="chart-empty">暂无数据</div>
    </div>
  </div>
</template>

<style scoped>
.chart-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-4);
}

.chart-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
}

.chart-hint {
  font-size: 12px;
  color: var(--text-tertiary);
}

.chart-wrapper {
  flex: 1;
  min-height: 240px;
}

.echarts-instance {
  width: 100%;
  height: 100%;
  min-height: 240px;
}

.chart-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 240px;
  color: var(--text-tertiary);
  font-size: 15px;
}
</style>
