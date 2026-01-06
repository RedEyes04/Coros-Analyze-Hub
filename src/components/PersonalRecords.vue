<script setup>
import { computed } from 'vue'
import { useTrainingData } from '@/composables/useTrainingData'
import { formatPace, formatDuration } from '@/utils/dataProcessor'

const { rawData } = useTrainingData()

const records = computed(() => {
  const data = rawData.value
  if (!data || data.length === 0) {
    return {
      maxDistance: { value: '--', date: '' },
      maxLoad: { value: '--', date: '' },
      fastestPace: { value: '--', date: '' },
      longestDuration: { value: '--', date: '' }
    }
  }
  
  // 计算28天前的日期
  const today = new Date()
  const date28DaysAgo = new Date(today)
  date28DaysAgo.setDate(date28DaysAgo.getDate() - 28)
  const startDateNum = parseInt(
    `${date28DaysAgo.getFullYear()}${String(date28DaysAgo.getMonth() + 1).padStart(2, '0')}${String(date28DaysAgo.getDate()).padStart(2, '0')}`
  )
  
  // 过滤近28天数据
  const recentData = data.filter(d => d.date >= startDateNum)
  
  if (recentData.length === 0) {
    return {
      maxDistance: { value: '--', date: '' },
      maxLoad: { value: '--', date: '' },
      fastestPace: { value: '--', date: '' },
      longestDuration: { value: '--', date: '' }
    }
  }
  
  // 过滤有效跑步数据（至少1km）
  const validRuns = recentData.filter(d => d.distance > 1000)
  
  // 最远距离
  const maxDistanceRun = validRuns.length > 0 
    ? validRuns.reduce((max, d) => d.distance > max.distance ? d : max, validRuns[0])
    : null
  
  // 最高负荷
  const maxLoadRun = recentData.reduce((max, d) => 
    d.training_load > max.training_load ? d : max, recentData[0])
  
  // 最快配速（只看5km以上的跑步）
  const longRuns = validRuns.filter(d => d.distance >= 5000 && d.pace > 0)
  const fastestPaceRun = longRuns.length > 0 
    ? longRuns.reduce((min, d) => d.pace < min.pace ? d : min, longRuns[0])
    : null
  
  // 最长时长
  const longestRun = validRuns.length > 0
    ? validRuns.reduce((max, d) => d.duration > max.duration ? d : max, validRuns[0])
    : null
  
  const formatDate = (dateNum) => {
    const str = String(dateNum)
    return `${str.substring(4,6)}/${str.substring(6,8)}`
  }
  
  return {
    maxDistance: maxDistanceRun ? {
      value: (maxDistanceRun.distance / 1000).toFixed(1),
      unit: 'km',
      date: formatDate(maxDistanceRun.date)
    } : { value: '--', unit: '', date: '' },
    maxLoad: {
      value: maxLoadRun.training_load,
      unit: '',
      date: formatDate(maxLoadRun.date)
    },
    fastestPace: fastestPaceRun ? {
      value: formatPace(fastestPaceRun.pace),
      unit: '/km',
      date: formatDate(fastestPaceRun.date)
    } : { value: '--', unit: '', date: '' },
    longestDuration: longestRun ? {
      value: formatDuration(longestRun.duration),
      unit: '',
      date: formatDate(longestRun.date)
    } : { value: '--', unit: '', date: '' }
  }
})
</script>

<template>
  <div class="records-card">
    <div class="card-header">
      <h3 class="card-title">个人记录</h3>
      <span class="card-subtitle">近 28 天</span>
    </div>
    
    <div class="records-list">
      <div class="record-item">
        <div class="record-icon icon-distance">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
          </svg>
        </div>
        <div class="record-info">
          <div class="record-label">最远距离</div>
          <div class="record-value">
            {{ records.maxDistance.value }}
            <span class="record-unit">{{ records.maxDistance.unit }}</span>
          </div>
        </div>
        <div class="record-date">{{ records.maxDistance.date }}</div>
      </div>
      
      <div class="record-item">
        <div class="record-icon icon-load">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>
          </svg>
        </div>
        <div class="record-info">
          <div class="record-label">最高负荷</div>
          <div class="record-value">{{ records.maxLoad.value }}</div>
        </div>
        <div class="record-date">{{ records.maxLoad.date }}</div>
      </div>
      
      <div class="record-item">
        <div class="record-icon icon-pace">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12 6 12 12 16 14"/>
          </svg>
        </div>
        <div class="record-info">
          <div class="record-label">最快配速</div>
          <div class="record-value">
            {{ records.fastestPace.value }}
            <span class="record-unit">{{ records.fastestPace.unit }}</span>
          </div>
        </div>
        <div class="record-date">{{ records.fastestPace.date }}</div>
      </div>
      
      <div class="record-item">
        <div class="record-icon icon-duration">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="2" x2="12" y2="6"/>
            <line x1="12" y1="18" x2="12" y2="22"/>
            <line x1="4.93" y1="4.93" x2="7.76" y2="7.76"/>
            <line x1="16.24" y1="16.24" x2="19.07" y2="19.07"/>
            <line x1="2" y1="12" x2="6" y2="12"/>
            <line x1="18" y1="12" x2="22" y2="12"/>
            <line x1="4.93" y1="19.07" x2="7.76" y2="16.24"/>
            <line x1="16.24" y1="7.76" x2="19.07" y2="4.93"/>
          </svg>
        </div>
        <div class="record-info">
          <div class="record-label">最长时长</div>
          <div class="record-value">{{ records.longestDuration.value }}</div>
        </div>
        <div class="record-date">{{ records.longestDuration.date }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.records-card {
  /* 自适应高度 */
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: var(--space-4);
}

.card-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
}

.card-subtitle {
  font-size: 12px;
  color: var(--text-tertiary);
}

.records-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.record-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: 10px 12px;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  transition: background var(--transition-fast);
}

.record-item:hover {
  background: var(--bg-tertiary);
}

.record-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  flex-shrink: 0;
}

.record-icon svg {
  width: 18px;
  height: 18px;
}

/* Icon Colors */
.icon-distance {
  background: rgba(0, 113, 227, 0.1);
  color: #0071e3;
}

.icon-load {
  background: rgba(255, 149, 0, 0.1);
  color: #ff9500;
}

.icon-pace {
  background: rgba(52, 199, 89, 0.1);
  color: #34c759;
}

.icon-duration {
  background: rgba(175, 82, 222, 0.1);
  color: #af52de;
}

.record-info {
  flex: 1;
  min-width: 0;
}

.record-label {
  font-size: 11px;
  color: var(--text-tertiary);
  margin-bottom: 1px;
}

.record-value {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
}

.record-unit {
  font-size: 12px;
  font-weight: 400;
  color: var(--text-secondary);
}

.record-date {
  font-size: 11px;
  color: var(--text-tertiary);
  flex-shrink: 0;
}
</style>
