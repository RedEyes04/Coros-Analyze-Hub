<script setup>
import { ref, computed } from 'vue'
import { 
  NButton, 
  NInput, 
  NSelect,
  NTabs,
  NTabPane,
  useMessage
} from 'naive-ui'
import { useTrainingData } from '@/composables/useTrainingData'

const message = useMessage()
const { rawData, acwrMetrics, aggregatedData } = useTrainingData()

const targetGoal = ref('')
const trainingPhase = ref(null)
const isLoading = ref(false)
const aiResponse = ref(null)
const apiKey = ref(import.meta.env.VITE_QWEN_API_KEY || '')
const activeWeek = ref('week1')

const phaseOptions = [
  { label: '基础期 · 有氧建设', value: 'base' },
  { label: '强化期 · 专项训练', value: 'build' },
  { label: '竞赛期 · 赛前调整', value: 'peak' },
  { label: '冬训期 · 耐力储备', value: 'winter' },
  { label: '恢复期 · 调整减量', value: 'recovery' }
]

// 计算近期统计数据
const recentStats = computed(() => {
  const data = aggregatedData.value
  if (!data || data.length === 0) return null
  
  const recent7 = data.slice(-7)
  const distance7 = recent7.reduce((sum, d) => sum + d.distance, 0)
  
  const recent28 = data.slice(-28)
  const distance28 = recent28.reduce((sum, d) => sum + d.distance, 0)
  
  return {
    distance7: distance7.toFixed(1),
    distance28: distance28.toFixed(1),
    avgDistancePerWeek: (distance28 / 4).toFixed(1)
  }
})

// 生成 4 周计划的 Prompt
function generatePrompt() {
  const recentData = rawData.value.slice(0, 10)
  const phaseText = phaseOptions.find(p => p.value === trainingPhase.value)?.label || '未指定'
  
  const recentTraining = recentData.map(a => {
    const dateStr = String(a.date)
    const date = `${dateStr.slice(4,6)}/${dateStr.slice(6,8)}`
    return `${date}: ${a.name}, ${(a.distance/1000).toFixed(1)}km, 负荷${a.training_load}`
  }).join('\n')
  
  return `你是一位专业的马拉松教练。请根据以下训练数据，制定一个4周的小周期训练计划。

## 运动员信息
- 目标成绩：${targetGoal.value}
- 当前阶段：${phaseText}

## 近期训练统计
- 近7天跑量：${recentStats.value?.distance7 || 0} km
- 近28天跑量：${recentStats.value?.distance28 || 0} km
- 周均跑量：${recentStats.value?.avgDistancePerWeek || 0} km

## 受伤风险评估
- ACWR 比率：${acwrMetrics.value.ratio}
- 风险等级：${acwrMetrics.value.riskText}
- 急性负荷(7天)：${acwrMetrics.value.acuteLoad}
- 慢性负荷(周均)：${acwrMetrics.value.chronicLoad}

## 最近训练记录
${recentTraining}

请制定4周小周期训练计划，要求：
1. 每周7天的具体训练安排
2. 遵循周期化原则（负荷递增+恢复周）
3. 考虑ACWR风险，合理控制负荷增长

回复格式要求（严格遵守）：
===第1周===
周一: [训练类型] [距离/时长] [说明]
周二: [训练类型] [距离/时长] [说明]
周三: [训练类型] [距离/时长] [说明]
周四: [训练类型] [距离/时长] [说明]
周五: [训练类型] [距离/时长] [说明]
周六: [训练类型] [距离/时长] [说明]
周日: [训练类型] [距离/时长] [说明]
本周重点: xxx
本周跑量: xxkm

===第2周===
(同上格式)

===第3周===
(同上格式)

===第4周===
(同上格式)

===训练建议===
1. xxx
2. xxx
3. xxx`
}

// 调用通义千问 API
async function callQwenAPI() {
  if (!targetGoal.value) {
    message.warning('请输入目标成绩')
    return
  }
  
  if (!apiKey.value || apiKey.value === 'YOUR_API_KEY') {
    message.warning('请先配置 API Key')
    return
  }
  
  isLoading.value = true
  aiResponse.value = null
  
  try {
    const prompt = generatePrompt()
    
    const response = await fetch('https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey.value}`
      },
      body: JSON.stringify({
        model: 'qwen-plus',
        messages: [
          {
            role: 'system',
            content: '你是一位专业的马拉松教练和运动科学专家，擅长制定周期化训练计划。回答要简洁实用，严格按照要求的格式输出。'
          },
          {
            role: 'user',
            content: prompt
          }
        ],
        temperature: 0.7,
        max_tokens: 2000
      })
    })
    
    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.error?.message || `API 请求失败: ${response.status}`)
    }
    
    const data = await response.json()
    const content = data.choices?.[0]?.message?.content
    
    if (content) {
      aiResponse.value = {
        raw: content,
        parsed: parse4WeekPlan(content)
      }
      message.success('4周训练计划生成成功！')
    } else {
      throw new Error('未收到有效回复')
    }
    
  } catch (error) {
    console.error('AI 调用失败:', error)
    message.error(`生成失败: ${error.message}`)
  } finally {
    isLoading.value = false
  }
}

// 解析 4 周计划
function parse4WeekPlan(content) {
  const weeks = []
  const tips = []
  
  // 按周分割
  const weekMatches = content.split(/===第(\d)周===/)
  
  for (let i = 1; i < weekMatches.length; i += 2) {
    const weekNum = weekMatches[i]
    const weekContent = weekMatches[i + 1] || ''
    
    const days = []
    const dayNames = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    
    dayNames.forEach(dayName => {
      const regex = new RegExp(`${dayName}[：:]\s*(.+)`, 'i')
      const match = weekContent.match(regex)
      if (match) {
        const content = match[1].trim()
        days.push({
          day: dayName,
          content: content,
          type: getTrainingType(content)
        })
      }
    })
    
    // 提取本周重点和跑量
    const focusMatch = weekContent.match(/本周重点[：:]\s*(.+)/i)
    const mileageMatch = weekContent.match(/本周跑量[：:]\s*(\d+)/i)
    
    weeks.push({
      weekNum: parseInt(weekNum),
      days,
      focus: focusMatch ? focusMatch[1].trim() : '',
      mileage: mileageMatch ? mileageMatch[1] : ''
    })
  }
  
  // 提取训练建议
  const tipsMatch = content.match(/===训练建议===([\s\S]*?)$/i)
  if (tipsMatch) {
    const tipsContent = tipsMatch[1]
    const tipLines = tipsContent.match(/\d+[.、]\s*(.+)/g)
    if (tipLines) {
      tipLines.forEach(line => {
        tips.push(line.replace(/^\d+[.、]\s*/, '').trim())
      })
    }
  }
  
  return { weeks, tips, raw: content }
}

// 根据内容判断训练类型
function getTrainingType(content) {
  const lower = content.toLowerCase()
  if (lower.includes('休息') || lower.includes('rest')) return 'rest'
  if (lower.includes('恢复') || lower.includes('轻松')) return 'easy'
  if (lower.includes('节奏') || lower.includes('tempo')) return 'tempo'
  if (lower.includes('间歇') || lower.includes('速度')) return 'interval'
  if (lower.includes('长距离') || lower.includes('lsd') || lower.includes('长跑')) return 'long'
  if (lower.includes('力量') || lower.includes('核心')) return 'strength'
  return 'easy'
}

// 获取训练类型颜色
function getTypeColor(type) {
  const colors = {
    rest: { bg: '#f5f5f7', text: '#86868b' },
    easy: { bg: '#e3f9e5', text: '#1e7e34' },
    tempo: { bg: '#fff3e0', text: '#e65100' },
    interval: { bg: '#ffebee', text: '#c62828' },
    long: { bg: '#e3f2fd', text: '#1565c0' },
    strength: { bg: '#f3e5f5', text: '#7b1fa2' }
  }
  return colors[type] || colors.easy
}

// 生成 4 周日历日期
const calendarDates = computed(() => {
  const today = new Date()
  // 找到下周一
  const dayOfWeek = today.getDay()
  const daysUntilMonday = dayOfWeek === 0 ? 1 : 8 - dayOfWeek
  const startDate = new Date(today)
  startDate.setDate(today.getDate() + daysUntilMonday)
  
  const weeks = []
  for (let w = 0; w < 4; w++) {
    const weekDates = []
    for (let d = 0; d < 7; d++) {
      const date = new Date(startDate)
      date.setDate(startDate.getDate() + w * 7 + d)
      weekDates.push({
        day: date.getDate(),
        month: date.getMonth() + 1,
        full: date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
      })
    }
    weeks.push(weekDates)
  }
  return weeks
})

function reset() {
  aiResponse.value = null
  targetGoal.value = ''
  trainingPhase.value = null
  activeWeek.value = 'week1'
}
</script>

<template>
  <div class="ai-plan">
    <div class="card-header">
      <h3 class="card-title">AI 训练计划</h3>
      <span class="powered-by">4周小周期</span>
    </div>

    <!-- API Key 提示 -->
    <div v-if="!apiKey || apiKey === 'YOUR_API_KEY'" class="api-hint">
      <p>请配置通义千问 API Key</p>
    </div>

    <!-- Input Form -->
    <div v-else-if="!aiResponse" class="input-form">
      <div class="form-row">
        <div class="form-group">
          <label>目标成绩</label>
          <n-input 
            v-model:value="targetGoal" 
            placeholder="如：全马 3:00"
            :disabled="isLoading"
          />
        </div>
        
        <div class="form-group">
          <label>训练阶段</label>
          <n-select 
            v-model:value="trainingPhase" 
            :options="phaseOptions"
            placeholder="选择阶段"
            :disabled="isLoading"
          />
        </div>
      </div>
      
      <n-button 
        type="primary" 
        block 
        :loading="isLoading"
        @click="callQwenAPI"
        class="submit-btn"
      >
        {{ isLoading ? '正在生成 4 周计划...' : '生成 4 周训练计划' }}
      </n-button>
    </div>

    <!-- 4 Week Plan Result -->
    <div v-else class="plan-result">
      <div class="result-header">
        <div class="result-title">
          <span>4 周训练计划</span>
          <span class="result-meta">目标：{{ targetGoal }}</span>
        </div>
        <button class="reset-btn" @click="reset">重新生成</button>
      </div>

      <!-- Week Tabs -->
      <div class="week-tabs">
        <button 
          v-for="(week, idx) in aiResponse.parsed.weeks" 
          :key="idx"
          class="week-tab"
          :class="{ active: activeWeek === `week${idx + 1}` }"
          @click="activeWeek = `week${idx + 1}`"
        >
          <span class="tab-week">第{{ week.weekNum }}周</span>
          <span class="tab-mileage" v-if="week.mileage">{{ week.mileage }}km</span>
        </button>
      </div>

      <!-- Calendar View -->
      <div class="calendar-view">
        <div class="calendar-header">
          <span v-for="d in ['一', '二', '三', '四', '五', '六', '日']" :key="d">周{{ d }}</span>
        </div>
        
        <template v-for="(week, weekIdx) in aiResponse.parsed.weeks" :key="weekIdx">
          <div 
            v-show="activeWeek === `week${weekIdx + 1}`"
            class="calendar-week"
          >
            <!-- 日期行 -->
            <div class="calendar-dates">
              <span v-for="(date, i) in calendarDates[weekIdx]" :key="i" class="date-cell">
                {{ date.full }}
              </span>
            </div>
            
            <!-- 训练内容行 -->
            <div class="calendar-content">
              <div 
                v-for="(day, dayIdx) in week.days" 
                :key="dayIdx"
                class="day-card"
                :style="{ 
                  background: getTypeColor(day.type).bg,
                  borderLeftColor: getTypeColor(day.type).text
                }"
              >
                <div class="day-content" :style="{ color: getTypeColor(day.type).text }">
                  {{ day.content }}
                </div>
              </div>
            </div>
            
            <!-- 本周重点 -->
            <div class="week-focus" v-if="week.focus">
              <span class="focus-label">本周重点</span>
              <span class="focus-text">{{ week.focus }}</span>
            </div>
          </div>
        </template>
      </div>

      <!-- 训练建议 -->
      <div v-if="aiResponse.parsed.tips.length > 0" class="tips-section">
        <div class="tips-title">训练建议</div>
        <ul class="tips-list">
          <li v-for="(tip, i) in aiResponse.parsed.tips" :key="i">{{ tip }}</li>
        </ul>
      </div>

      <!-- 原始回复 -->
      <details class="raw-response">
        <summary>查看完整回复</summary>
        <pre>{{ aiResponse.raw }}</pre>
      </details>
    </div>
  </div>
</template>

<style scoped>
.ai-plan {
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-5);
}

.card-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
}

.powered-by {
  font-size: 11px;
  color: var(--blue);
  background: rgba(0, 113, 227, 0.1);
  padding: 3px 10px;
  border-radius: 12px;
  font-weight: 500;
}

/* API Hint */
.api-hint {
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  font-size: 13px;
  color: var(--text-secondary);
  text-align: center;
}

/* Form */
.input-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.form-group label {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
}

.submit-btn {
  margin-top: var(--space-2);
  height: 44px;
  border-radius: var(--radius-md);
  font-weight: 500;
}

/* Result */
.plan-result {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.result-title {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.result-title span:first-child {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
}

.result-meta {
  font-size: 12px;
  color: var(--text-tertiary);
}

.reset-btn {
  font-size: 13px;
  color: var(--blue);
  background: none;
  border: none;
  cursor: pointer;
}

.reset-btn:hover {
  text-decoration: underline;
}

/* Week Tabs */
.week-tabs {
  display: flex;
  gap: var(--space-2);
  border-bottom: 1px solid var(--border-color-light);
  padding-bottom: var(--space-3);
}

.week-tab {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  padding: var(--space-2) var(--space-4);
  background: var(--bg-secondary);
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.week-tab:hover {
  background: var(--bg-tertiary);
}

.week-tab.active {
  background: var(--blue);
}

.tab-week {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
}

.week-tab.active .tab-week {
  color: white;
}

.tab-mileage {
  font-size: 11px;
  color: var(--text-tertiary);
}

.week-tab.active .tab-mileage {
  color: rgba(255,255,255,0.8);
}

/* Calendar View */
.calendar-view {
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  padding: var(--space-4);
}

.calendar-header {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: var(--space-2);
  margin-bottom: var(--space-2);
}

.calendar-header span {
  text-align: center;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-tertiary);
}

.calendar-week {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.calendar-dates {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: var(--space-2);
}

.date-cell {
  text-align: center;
  font-size: 11px;
  color: var(--text-secondary);
}

.calendar-content {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: var(--space-2);
}

.day-card {
  padding: var(--space-3);
  border-radius: var(--radius-sm);
  border-left: 3px solid;
  min-height: 80px;
}

.day-content {
  font-size: 12px;
  line-height: 1.5;
  word-break: break-word;
}

.week-focus {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  background: var(--bg-primary);
  border-radius: var(--radius-sm);
  margin-top: var(--space-2);
}

.focus-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--blue);
  white-space: nowrap;
}

.focus-text {
  font-size: 13px;
  color: var(--text-secondary);
}

/* Tips */
.tips-section {
  margin-top: var(--space-2);
}

.tips-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: var(--space-2);
}

.tips-list {
  margin: 0;
  padding-left: var(--space-5);
}

.tips-list li {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: var(--space-1);
}

.tips-list li::marker {
  color: var(--green);
}

/* Raw Response */
.raw-response {
  margin-top: var(--space-2);
  font-size: 12px;
  color: var(--text-tertiary);
}

.raw-response summary {
  cursor: pointer;
  padding: var(--space-2) 0;
}

.raw-response pre {
  background: var(--bg-secondary);
  padding: var(--space-3);
  border-radius: var(--radius-sm);
  white-space: pre-wrap;
  word-break: break-word;
  font-size: 11px;
  line-height: 1.5;
  max-height: 200px;
  overflow-y: auto;
  margin-top: var(--space-2);
}

/* Responsive */
@media (max-width: 900px) {
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .calendar-content {
    grid-template-columns: repeat(4, 1fr);
  }
  
  .calendar-header,
  .calendar-dates {
    display: none;
  }
  
  .day-card::before {
    content: attr(data-day);
    font-size: 11px;
    font-weight: 600;
    display: block;
    margin-bottom: 4px;
  }
}
</style>
