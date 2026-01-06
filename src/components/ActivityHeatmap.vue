<script setup>
import { computed, ref } from 'vue'
import { NTooltip } from 'naive-ui'
import { useTrainingData } from '@/composables/useTrainingData'

const { aggregatedData } = useTrainingData()

const currentDate = ref(new Date())

function prevMonth() {
  const d = new Date(currentDate.value)
  d.setMonth(d.getMonth() - 1)
  currentDate.value = d
}

function nextMonth() {
  const d = new Date(currentDate.value)
  d.setMonth(d.getMonth() + 1)
  currentDate.value = d
}

const monthTitle = computed(() => {
  return currentDate.value.toLocaleDateString('zh-CN', { 
    year: 'numeric', 
    month: 'long' 
  })
})

const calendarDays = computed(() => {
  const year = currentDate.value.getFullYear()
  const month = currentDate.value.getMonth()
  
  const dataMap = new Map()
  aggregatedData.value.forEach(item => {
    dataMap.set(item.date, item)
  })
  
  const firstDay = new Date(year, month, 1)
  const lastDay = new Date(year, month + 1, 0)
  
  let startWeekday = firstDay.getDay()
  startWeekday = startWeekday === 0 ? 6 : startWeekday - 1
  
  const days = []
  
  for (let i = 0; i < startWeekday; i++) {
    days.push({ empty: true })
  }
  
  for (let day = 1; day <= lastDay.getDate(); day++) {
    const dateNum = parseInt(
      `${year}${String(month + 1).padStart(2, '0')}${String(day).padStart(2, '0')}`
    )
    
    const activity = dataMap.get(dateNum)
    const isToday = isSameDay(new Date(year, month, day), new Date())
    
    days.push({
      day,
      dateNum,
      isToday,
      hasActivity: !!activity,
      distance: activity ? activity.distance : 0,
      trainingLoad: activity ? activity.trainingLoad : 0,
      level: activity ? getLevel(activity.trainingLoad) : 0,
      fullDate: new Date(year, month, day).toLocaleDateString('zh-CN', {
        month: 'long',
        day: 'numeric',
        weekday: 'short'
      })
    })
  }
  
  return days
})

const monthStats = computed(() => {
  const year = currentDate.value.getFullYear()
  const month = currentDate.value.getMonth()
  
  const monthStart = parseInt(`${year}${String(month + 1).padStart(2, '0')}01`)
  const monthEnd = parseInt(`${year}${String(month + 1).padStart(2, '0')}31`)
  
  const monthData = aggregatedData.value.filter(
    d => d.date >= monthStart && d.date <= monthEnd
  )
  
  const totalDistance = monthData.reduce((sum, d) => sum + d.distance, 0)
  const trainingDays = monthData.length
  
  return {
    totalDistance: totalDistance.toFixed(0),
    trainingDays
  }
})

function isSameDay(d1, d2) {
  return d1.getFullYear() === d2.getFullYear() &&
         d1.getMonth() === d2.getMonth() &&
         d1.getDate() === d2.getDate()
}

function getLevel(load) {
  if (load === 0) return 0
  if (load < 50) return 1
  if (load < 100) return 2
  if (load < 200) return 3
  return 4
}

const weekdays = ['一', '二', '三', '四', '五', '六', '日']
</script>

<template>
  <div class="calendar-compact">
    <!-- Header -->
    <div class="cal-header">
      <button class="nav-btn" @click="prevMonth">‹</button>
      <span class="month-title">{{ monthTitle }}</span>
      <button class="nav-btn" @click="nextMonth">›</button>
    </div>

    <!-- Weekdays -->
    <div class="weekdays">
      <span v-for="d in weekdays" :key="d">{{ d }}</span>
    </div>

    <!-- Days Grid -->
    <div class="days-grid">
      <template v-for="(day, i) in calendarDays" :key="i">
        <div v-if="day.empty" class="day empty"></div>
        <n-tooltip v-else :show-arrow="false" placement="top">
          <template #trigger>
            <div 
              class="day"
              :class="[`level-${day.level}`, { today: day.isToday }]"
            >
              {{ day.day }}
            </div>
          </template>
          <!-- Tooltip Content -->
          <div class="tip-card">
            <div class="tip-date">{{ day.fullDate }}</div>
            <div v-if="day.hasActivity" class="tip-stats">
              <div class="tip-row">
                <span class="tip-icon">🏃</span>
                <span class="tip-value">{{ day.distance.toFixed(1) }} km</span>
              </div>
              <div class="tip-row">
                <span class="tip-icon">💪</span>
                <span class="tip-value">负荷 {{ day.trainingLoad }}</span>
              </div>
            </div>
            <div v-else class="tip-rest">
              <span class="tip-icon">😴</span>
              <span>休息日</span>
            </div>
          </div>
        </n-tooltip>
      </template>
    </div>

    <!-- Stats -->
    <div class="cal-footer">
      <div class="footer-stat">
        <span class="footer-value">{{ monthStats.totalDistance }}</span>
        <span class="footer-label">km</span>
      </div>
      <div class="footer-stat">
        <span class="footer-value">{{ monthStats.trainingDays }}</span>
        <span class="footer-label">天训练</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.calendar-compact {
  width: 100%;
}

.cal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-3);
}

.month-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
}

.nav-btn {
  width: 28px;
  height: 28px;
  border: none;
  background: var(--bg-tertiary);
  color: var(--text-primary);
  border-radius: 8px;
  cursor: pointer;
  font-size: 18px;
  font-weight: 500;
  line-height: 1;
  transition: all var(--transition-fast);
}

.nav-btn:hover {
  background: var(--gray-200);
}

.weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 3px;
  margin-bottom: 6px;
}

.weekdays span {
  text-align: center;
  font-size: 11px;
  font-weight: 500;
  color: var(--text-tertiary);
  padding: 4px 0;
}

.days-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 3px;
}

.day {
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  border-radius: 6px;
  cursor: pointer;
  transition: transform var(--transition-fast);
}

.day:not(.empty):hover {
  transform: scale(1.15);
  z-index: 1;
}

.day.empty {
  background: transparent;
  cursor: default;
}

/* 今日样式 */
.day.today {
  box-shadow: inset 0 0 0 2px var(--blue);
}

/* Level 颜色 - 高对比度 */
.day.level-0 {
  background: var(--gray-100);
  color: var(--gray-400);
}

.day.level-1 {
  background: #e8f5e9;
  color: #2e7d32;
}

.day.level-2 {
  background: #c8e6c9;
  color: #1b5e20;
}

.day.level-3 {
  background: #81c784;
  color: #ffffff;
  text-shadow: 0 1px 2px rgba(0,0,0,0.2);
}

.day.level-4 {
  background: #43a047;
  color: #ffffff;
  text-shadow: 0 1px 2px rgba(0,0,0,0.2);
}

/* Footer Stats */
.cal-footer {
  display: flex;
  justify-content: space-around;
  margin-top: var(--space-4);
  padding-top: var(--space-3);
  border-top: 1px solid var(--border-color-light);
}

.footer-stat {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.footer-value {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
}

.footer-label {
  font-size: 12px;
  color: var(--text-tertiary);
}

/* Tooltip Card */
.tip-card {
  padding: 4px;
  min-width: 140px;
}

.tip-date {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  padding-bottom: 8px;
  margin-bottom: 8px;
  border-bottom: 1px solid var(--border-color-light);
}

.tip-stats {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.tip-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.tip-icon {
  font-size: 14px;
}

.tip-value {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.tip-rest {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--text-secondary);
}
</style>
