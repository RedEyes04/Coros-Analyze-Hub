<script setup>
import { computed } from 'vue'
import { useTrainingData } from '@/composables/useTrainingData'
import { formatDuration } from '@/utils/dataProcessor'

const { aggregatedData, isLoading } = useTrainingData()

// 计算近 28 天的统计数据
const stats28Days = computed(() => {
  const today = new Date()
  const todayNum = parseInt(
    `${today.getFullYear()}${String(today.getMonth() + 1).padStart(2, '0')}${String(today.getDate()).padStart(2, '0')}`
  )
  
  // 28天前的日期
  const date28DaysAgo = new Date(today)
  date28DaysAgo.setDate(date28DaysAgo.getDate() - 28)
  const startDateNum = parseInt(
    `${date28DaysAgo.getFullYear()}${String(date28DaysAgo.getMonth() + 1).padStart(2, '0')}${String(date28DaysAgo.getDate()).padStart(2, '0')}`
  )
  
  // 过滤近28天数据
  const recentData = aggregatedData.value.filter(
    d => d.date >= startDateNum && d.date <= todayNum
  )
  
  if (recentData.length === 0) {
    return {
      totalDistance: 0,
      totalDuration: '0:00',
      totalTrainingLoad: 0,
      trainingDays: 0,
      avgDistancePerDay: 0
    }
  }
  
  const totalDistance = recentData.reduce((sum, d) => sum + d.distance, 0)
  const totalDuration = recentData.reduce((sum, d) => sum + d.duration, 0)
  const totalTrainingLoad = recentData.reduce((sum, d) => sum + d.trainingLoad, 0)
  
  return {
    totalDistance: totalDistance.toFixed(1),
    totalDuration: formatDuration(totalDuration),
    totalTrainingLoad,
    trainingDays: recentData.length,
    avgDistancePerDay: (totalDistance / 28).toFixed(1)
  }
})
</script>

<template>
  <div class="stats-overview">
    <!-- Main Stat -->
    <div class="main-stat animate-fade-in-up">
      <div class="stat-value-large">{{ stats28Days.totalDistance }}</div>
      <div class="stat-unit-large">公里</div>
      <div class="stat-description">近 28 天跑量</div>
    </div>
    
    <!-- Secondary Stats -->
    <div class="secondary-stats">
      <div class="stat-item animate-fade-in-up delay-1">
        <div class="stat-value-small">{{ stats28Days.trainingDays }}</div>
        <div class="stat-label">训练天数</div>
      </div>
      
      <div class="stat-divider"></div>
      
      <div class="stat-item animate-fade-in-up delay-2">
        <div class="stat-value-small">{{ stats28Days.totalDuration }}</div>
        <div class="stat-label">总时长</div>
      </div>
      
      <div class="stat-divider"></div>
      
      <div class="stat-item animate-fade-in-up delay-3">
        <div class="stat-value-small">{{ stats28Days.totalTrainingLoad }}</div>
        <div class="stat-label">训练负荷</div>
      </div>
      
      <div class="stat-divider"></div>
      
      <div class="stat-item animate-fade-in-up delay-4">
        <div class="stat-value-small">{{ stats28Days.avgDistancePerDay }}</div>
        <div class="stat-label">日均跑量 (km)</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.stats-overview {
  text-align: center;
  padding: var(--space-12) 0;
}

.main-stat {
  margin-bottom: var(--space-10);
}

.stat-value-large {
  font-size: 80px;
  font-weight: 600;
  letter-spacing: -0.04em;
  line-height: 1;
  color: var(--text-primary);
  display: inline;
}

.stat-unit-large {
  font-size: 32px;
  font-weight: 500;
  color: var(--text-secondary);
  display: inline;
  margin-left: var(--space-2);
}

.stat-description {
  font-size: 17px;
  color: var(--text-secondary);
  margin-top: var(--space-3);
}

.secondary-stats {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: var(--space-8);
  flex-wrap: wrap;
}

.stat-item {
  text-align: center;
  min-width: 100px;
}

.stat-value-small {
  font-size: 28px;
  font-weight: 600;
  letter-spacing: -0.02em;
  color: var(--text-primary);
  line-height: 1.2;
}

.stat-label {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: var(--space-1);
}

.stat-divider {
  width: 1px;
  height: 40px;
  background: var(--border-color);
}

@media (max-width: 768px) {
  .stat-value-large {
    font-size: 56px;
  }
  
  .stat-unit-large {
    font-size: 24px;
  }
  
  .secondary-stats {
    gap: var(--space-6);
  }
  
  .stat-divider {
    display: none;
  }
}
</style>
