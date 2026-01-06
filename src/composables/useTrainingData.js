import { ref, computed } from 'vue'
import { 
  aggregateByDate, 
  calculateACWR, 
  calculateStats,
  getRecentDays 
} from '@/utils/dataProcessor'

/**
 * 训练数据 Composable（单例模式）
 * 所有组件共享同一份数据
 */

// 模块级别的响应式状态（单例）
const rawData = ref([])
const aggregatedData = ref([])
const isLoading = ref(false)
const error = ref(null)
const isLoaded = ref(false)

/**
 * 加载训练数据
 */
async function loadData() {
  // 避免重复加载
  if (isLoaded.value) return
  
  isLoading.value = true
  error.value = null
  
  try {
    // 从 public 目录加载数据
    const response = await fetch('/activities_data.json')
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    rawData.value = data
    
    // 聚合数据
    aggregatedData.value = aggregateByDate(data)
    isLoaded.value = true
    
    console.log('✅ 训练数据加载成功:', {
      原始记录数: data.length,
      聚合后天数: aggregatedData.value.length
    })
    
  } catch (err) {
    console.error('❌ 加载训练数据失败:', err)
    error.value = err.message
  } finally {
    isLoading.value = false
  }
}

// ACWR 指标（计算属性）
const acwrMetrics = computed(() => {
  return calculateACWR(aggregatedData.value)
})

// 统计摘要
const stats = computed(() => {
  return calculateStats(aggregatedData.value)
})

// 最近7天数据
const recent7Days = computed(() => {
  return getRecentDays(aggregatedData.value, 7)
})

// 最近30天数据
const recent30Days = computed(() => {
  return getRecentDays(aggregatedData.value, 30)
})

// 图表数据：训练负荷
const trainingLoadChartData = computed(() => {
  const data = aggregatedData.value
  return {
    dates: data.map(d => d.dateFormatted),
    values: data.map(d => d.trainingLoad)
  }
})

// 图表数据：每日跑量
const distanceChartData = computed(() => {
  const data = aggregatedData.value
  return {
    dates: data.map(d => d.dateFormatted),
    values: data.map(d => d.distance)
  }
})

/**
 * 导出 composable 函数
 * 返回共享的响应式状态
 */
export function useTrainingData() {
  return {
    // State（共享）
    rawData,
    aggregatedData,
    isLoading,
    error,
    isLoaded,
    
    // Computed
    acwrMetrics,
    stats,
    recent7Days,
    recent30Days,
    trainingLoadChartData,
    distanceChartData,
    
    // Methods
    loadData
  }
}
