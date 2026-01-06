<script setup>
import { computed } from 'vue'
import { NTooltip } from 'naive-ui'
import { useTrainingData } from '@/composables/useTrainingData'

const { acwrMetrics, isLoading } = useTrainingData()

const riskLevelText = computed(() => {
  const level = acwrMetrics.value.riskLevel
  const texts = {
    low: '低风险',
    moderate: '适中',
    medium: '中等',
    high: '较高',
    critical: '高风险',
    unknown: '未知'
  }
  return texts[level] || texts.unknown
})

const progressStyle = computed(() => {
  const ratio = Math.min(acwrMetrics.value.ratio, 2)
  const percentage = (ratio / 2) * 100
  const circumference = 2 * Math.PI * 40
  const offset = circumference - (percentage / 100) * circumference
  
  return {
    strokeDasharray: `${circumference}`,
    strokeDashoffset: `${offset}`
  }
})

const riskColor = computed(() => {
  const level = acwrMetrics.value.riskLevel
  const colors = {
    low: '#34c759',
    moderate: '#a8d600',
    medium: '#ffcc00',
    high: '#ff9500',
    critical: '#ff3b30',
    unknown: '#86868b'
  }
  return colors[level] || colors.unknown
})
</script>

<template>
  <div class="acwr-card">
    <div class="card-header">
      <h3 class="card-title">受伤风险</h3>
      <n-tooltip placement="bottom" :show-arrow="false">
        <template #trigger>
          <button class="info-btn">?</button>
        </template>
        <div class="tooltip-formula">
          <div class="tooltip-title">ACWR 急慢性负荷比</div>
          <div class="formula-box">
            <div class="formula-row">
              <span class="formula-label">急性负荷</span>
              <span class="formula-eq">=</span>
              <span class="formula-value">近 7 天负荷总和</span>
            </div>
            <div class="formula-row">
              <span class="formula-label">慢性负荷</span>
              <span class="formula-eq">=</span>
              <span class="formula-value">近 28 天负荷 ÷ 4</span>
            </div>
            <div class="formula-divider"></div>
            <div class="formula-row main">
              <span class="formula-label">ACWR</span>
              <span class="formula-eq">=</span>
              <span class="formula-value">急性 ÷ 慢性</span>
            </div>
          </div>
          <div class="tooltip-hint">建议范围: 0.8 ~ 1.3</div>
        </div>
      </n-tooltip>
    </div>

    <div class="acwr-body">
      <!-- 左侧圆环 -->
      <div class="ratio-ring">
        <svg viewBox="0 0 100 100" class="ring-svg">
          <circle cx="50" cy="50" r="40" fill="none" stroke="#f0f0f0" stroke-width="6"/>
          <circle
            cx="50" cy="50" r="40"
            fill="none"
            :stroke="riskColor"
            stroke-width="6"
            stroke-linecap="round"
            :style="progressStyle"
            transform="rotate(-90 50 50)"
          />
        </svg>
        <div class="ring-content">
          <span class="ratio-value">{{ acwrMetrics.ratio.toFixed(2) }}</span>
        </div>
      </div>

      <!-- 右侧信息 -->
      <div class="acwr-info">
        <span class="risk-badge" :class="acwrMetrics.riskLevel">
          {{ riskLevelText }}
        </span>
        <p class="risk-text">{{ acwrMetrics.riskText }}</p>
      </div>
    </div>

    <!-- 底部数据 -->
    <div class="acwr-footer">
      <div class="footer-item">
        <span class="footer-value">{{ acwrMetrics.acuteLoad }}</span>
        <span class="footer-label">急性 (7天)</span>
      </div>
      <div class="footer-item">
        <span class="footer-value">{{ acwrMetrics.chronicLoad }}</span>
        <span class="footer-label">慢性 (周均)</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.acwr-card {
  /* 自适应高度，不设置 height: 100% */
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-4);
}

.card-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
}

.info-btn {
  width: 20px;
  height: 20px;
  border: 1.5px solid var(--text-tertiary);
  background: none;
  color: var(--text-tertiary);
  border-radius: 50%;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.info-btn:hover {
  border-color: var(--text-secondary);
  color: var(--text-secondary);
}

/* Body - 横向布局 */
.acwr-body {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  margin-bottom: var(--space-4);
}

/* Ring - 更小 */
.ratio-ring {
  position: relative;
  width: 90px;
  height: 90px;
  flex-shrink: 0;
}

.ring-svg {
  width: 100%;
  height: 100%;
}

.ring-svg circle {
  transition: stroke-dashoffset 0.6s ease;
}

.ring-content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.ratio-value {
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
}

/* Info */
.acwr-info {
  flex: 1;
}

.risk-text {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: var(--space-2);
  line-height: 1.4;
}

/* Footer */
.acwr-footer {
  display: flex;
  gap: var(--space-4);
  padding-top: var(--space-3);
  border-top: 1px solid var(--border-color-light);
}

.footer-item {
  flex: 1;
  text-align: center;
}

.footer-value {
  display: block;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
}

.footer-label {
  font-size: 11px;
  color: var(--text-tertiary);
}

/* Tooltip Formula */
.tooltip-formula {
  width: 220px;
}

.tooltip-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.formula-box {
  background: var(--bg-secondary);
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 10px;
}

.formula-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 6px;
}

.formula-row:last-child {
  margin-bottom: 0;
}

.formula-row.main {
  color: var(--text-primary);
  font-weight: 500;
}

.formula-label {
  min-width: 56px;
  color: var(--text-tertiary);
}

.formula-eq {
  color: var(--text-tertiary);
}

.formula-value {
  flex: 1;
}

.formula-divider {
  height: 1px;
  background: var(--border-color-light);
  margin: 8px 0;
}

.tooltip-hint {
  font-size: 12px;
  color: var(--green);
  font-weight: 500;
}
</style>
