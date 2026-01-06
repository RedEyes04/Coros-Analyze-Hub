<script setup>
import { computed } from 'vue'
import { useTrainingData } from '@/composables/useTrainingData'
import { formatPace, formatDuration } from '@/utils/dataProcessor'

const { rawData } = useTrainingData()

// 最近 8 条训练记录
const recentActivities = computed(() => {
  return rawData.value.slice(0, 8).map(activity => {
    const dateStr = String(activity.date)
    const year = dateStr.substring(0, 4)
    const month = dateStr.substring(4, 6)
    const day = dateStr.substring(6, 8)
    const date = new Date(year, month - 1, day)
    
    return {
      ...activity,
      dateFormatted: date.toLocaleDateString('zh-CN', { 
        month: 'short', 
        day: 'numeric',
        weekday: 'short'
      }),
      distanceKm: (activity.distance / 1000).toFixed(2),
      durationFormatted: formatDuration(activity.duration),
      paceFormatted: formatPace(activity.pace),
      intensityLevel: getIntensityLevel(activity.training_load)
    }
  })
})

function getIntensityLevel(load) {
  if (load < 50) return { text: '轻松', color: '#34c759' }
  if (load < 100) return { text: '中等', color: '#ff9500' }
  if (load < 200) return { text: '较高', color: '#ff6b00' }
  return { text: '高强度', color: '#ff3b30' }
}
</script>

<template>
  <div class="recent-activities">
    <div class="section-header">
      <h3 class="section-title">最近训练</h3>
    </div>
    
    <div class="activities-list">
      <div 
        v-for="(activity, index) in recentActivities" 
        :key="index"
        class="activity-item"
      >
        <div class="activity-date">
          <span class="date-text">{{ activity.dateFormatted }}</span>
        </div>
        
        <div class="activity-main">
          <div class="activity-name">{{ activity.name }}</div>
          <div class="activity-stats">
            <span class="stat">
              <strong>{{ activity.distanceKm }}</strong> km
            </span>
            <span class="stat-divider">·</span>
            <span class="stat">{{ activity.durationFormatted }}</span>
            <span class="stat-divider">·</span>
            <span class="stat">{{ activity.paceFormatted }} /km</span>
          </div>
        </div>
        
        <div class="activity-load">
          <span 
            class="load-badge"
            :style="{ background: activity.intensityLevel.color + '15', color: activity.intensityLevel.color }"
          >
            {{ activity.training_load }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.recent-activities {
  height: 100%;
}

.section-header {
  margin-bottom: var(--space-4);
}

.section-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
}

.activities-list {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-3) var(--space-4);
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  transition: background var(--transition-fast);
}

.activity-item:hover {
  background: var(--bg-tertiary);
}

.activity-date {
  min-width: 70px;
}

.date-text {
  font-size: 12px;
  color: var(--text-secondary);
}

.activity-main {
  flex: 1;
  min-width: 0;
}

.activity-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 2px;
}

.activity-stats {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: 12px;
  color: var(--text-secondary);
}

.stat strong {
  color: var(--text-primary);
  font-weight: 600;
}

.stat-divider {
  color: var(--text-tertiary);
}

.activity-load {
  min-width: 44px;
  text-align: right;
}

.load-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 600;
}
</style>
