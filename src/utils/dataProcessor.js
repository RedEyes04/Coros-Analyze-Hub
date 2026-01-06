/**
 * 数据处理工具函数
 * 处理 activities_data.json 中的训练数据
 */

/**
 * 将 YYYYMMDD 格式的日期转换为 Date 对象
 * @param {number} dateNum - YYYYMMDD 格式的日期数字
 * @returns {Date}
 */
export function parseDate(dateNum) {
  const str = String(dateNum)
  const year = parseInt(str.substring(0, 4))
  const month = parseInt(str.substring(4, 6)) - 1 // 月份从0开始
  const day = parseInt(str.substring(6, 8))
  return new Date(year, month, day)
}

/**
 * 格式化日期为显示字符串
 * @param {number} dateNum - YYYYMMDD 格式的日期数字
 * @param {string} format - 格式类型 'short' | 'full' | 'chart'
 * @returns {string}
 */
export function formatDate(dateNum, format = 'short') {
  const date = parseDate(dateNum)
  
  const options = {
    short: { month: '2-digit', day: '2-digit' },
    full: { year: 'numeric', month: '2-digit', day: '2-digit' },
    chart: { month: 'short', day: 'numeric' }
  }
  
  return date.toLocaleDateString('zh-CN', options[format] || options.short)
}

/**
 * 将距离（米）转换为公里
 * @param {number} meters - 距离（米）
 * @returns {number} 距离（公里，保留2位小数）
 */
export function metersToKm(meters) {
  return Math.round((meters / 1000) * 100) / 100
}

/**
 * 将配速（秒/公里）格式化为 mm:ss
 * @param {number} paceSeconds - 配速（秒/公里）
 * @returns {string}
 */
export function formatPace(paceSeconds) {
  if (!paceSeconds || paceSeconds === 0) return '--'
  const minutes = Math.floor(paceSeconds / 60)
  const seconds = paceSeconds % 60
  return `${minutes}'${seconds.toString().padStart(2, '0')}"`
}

/**
 * 将持续时间（秒）格式化为 HH:MM:SS 或 MM:SS
 * @param {number} seconds - 持续时间（秒）
 * @returns {string}
 */
export function formatDuration(seconds) {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  
  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }
  return `${minutes}:${secs.toString().padStart(2, '0')}`
}

/**
 * 按日期聚合训练数据
 * 同一天的多次训练合并计算
 * @param {Array} activities - 原始活动数据
 * @returns {Array} 聚合后的数据，按日期排序
 */
export function aggregateByDate(activities) {
  const grouped = {}
  
  activities.forEach(activity => {
    const dateKey = activity.date
    
    if (!grouped[dateKey]) {
      grouped[dateKey] = {
        date: dateKey,
        totalDistance: 0,
        totalDuration: 0,
        totalTrainingLoad: 0,
        avgHrSum: 0,
        avgHrCount: 0,
        activities: []
      }
    }
    
    grouped[dateKey].totalDistance += activity.distance
    grouped[dateKey].totalDuration += activity.duration
    grouped[dateKey].totalTrainingLoad += activity.training_load
    grouped[dateKey].avgHrSum += activity.avg_hr * activity.duration // 按时间加权
    grouped[dateKey].avgHrCount += activity.duration
    grouped[dateKey].activities.push(activity)
  })
  
  // 转换为数组并计算派生值
  return Object.values(grouped)
    .map(day => ({
      date: day.date,
      dateFormatted: formatDate(day.date),
      dateFull: formatDate(day.date, 'full'),
      distance: metersToKm(day.totalDistance),
      distanceRaw: day.totalDistance,
      duration: day.totalDuration,
      durationFormatted: formatDuration(day.totalDuration),
      trainingLoad: day.totalTrainingLoad,
      avgHr: Math.round(day.avgHrSum / day.avgHrCount),
      activityCount: day.activities.length,
      activities: day.activities
    }))
    .sort((a, b) => a.date - b.date)
}

/**
 * 计算 ACWR（急慢性负荷比）指标
 * @param {Array} aggregatedData - 按日期聚合后的数据
 * @returns {Object} ACWR 指标
 */
export function calculateACWR(aggregatedData) {
  if (!aggregatedData || aggregatedData.length === 0) {
    return {
      acuteLoad: 0,
      chronicLoad: 0,
      ratio: 0,
      riskScore: 0,
      riskLevel: 'unknown',
      riskText: '数据不足'
    }
  }
  
  // 获取今天的日期
  const today = new Date()
  const todayNum = parseInt(
    `${today.getFullYear()}${String(today.getMonth() + 1).padStart(2, '0')}${String(today.getDate()).padStart(2, '0')}`
  )
  
  // 计算日期范围
  const getDaysAgo = (days) => {
    const date = new Date(today)
    date.setDate(date.getDate() - days)
    return parseInt(
      `${date.getFullYear()}${String(date.getMonth() + 1).padStart(2, '0')}${String(date.getDate()).padStart(2, '0')}`
    )
  }
  
  const sevenDaysAgo = getDaysAgo(7)
  const twentyEightDaysAgo = getDaysAgo(28)
  
  // 计算急性负荷（最近7天）
  const acuteLoad = aggregatedData
    .filter(d => d.date >= sevenDaysAgo && d.date <= todayNum)
    .reduce((sum, d) => sum + d.trainingLoad, 0)
  
  // 计算慢性负荷（最近28天的周平均）
  const chronicLoadTotal = aggregatedData
    .filter(d => d.date >= twentyEightDaysAgo && d.date <= todayNum)
    .reduce((sum, d) => sum + d.trainingLoad, 0)
  const chronicLoad = chronicLoadTotal / 4 // 4周平均
  
  // 计算比率
  const ratio = chronicLoad > 0 ? acuteLoad / chronicLoad : 0
  
  // 计算风险评分和等级
  let riskScore, riskLevel, riskText
  
  if (ratio <= 0.8) {
    riskScore = 10
    riskLevel = 'low'
    riskText = '训练量偏保守'
  } else if (ratio <= 1.0) {
    riskScore = 20
    riskLevel = 'moderate'
    riskText = '训练状态良好'
  } else if (ratio <= 1.3) {
    riskScore = 40
    riskLevel = 'medium'
    riskText = '负荷适中增长'
  } else if (ratio <= 1.5) {
    riskScore = 70
    riskLevel = 'high'
    riskText = '负荷增长较快'
  } else {
    riskScore = 90
    riskLevel = 'critical'
    riskText = '高风险，建议减量'
  }
  
  return {
    acuteLoad: Math.round(acuteLoad),
    chronicLoad: Math.round(chronicLoad),
    ratio: Math.round(ratio * 100) / 100,
    riskScore,
    riskLevel,
    riskText
  }
}

/**
 * 计算统计摘要
 * @param {Array} aggregatedData - 按日期聚合后的数据
 * @returns {Object} 统计摘要
 */
export function calculateStats(aggregatedData) {
  if (!aggregatedData || aggregatedData.length === 0) {
    return {
      totalDistance: 0,
      totalDuration: 0,
      totalTrainingLoad: 0,
      avgPace: 0,
      avgHr: 0,
      trainingDays: 0,
      activitiesCount: 0
    }
  }
  
  const totalDistance = aggregatedData.reduce((sum, d) => sum + d.distanceRaw, 0)
  const totalDuration = aggregatedData.reduce((sum, d) => sum + d.duration, 0)
  const totalTrainingLoad = aggregatedData.reduce((sum, d) => sum + d.trainingLoad, 0)
  const activitiesCount = aggregatedData.reduce((sum, d) => sum + d.activityCount, 0)
  
  // 加权平均心率
  const avgHr = aggregatedData.reduce((sum, d) => sum + d.avgHr * d.duration, 0) / totalDuration
  
  // 平均配速（秒/公里）
  const avgPace = totalDistance > 0 ? (totalDuration / (totalDistance / 1000)) : 0
  
  return {
    totalDistance: metersToKm(totalDistance),
    totalDuration,
    totalDurationFormatted: formatDuration(totalDuration),
    totalTrainingLoad,
    avgPace: Math.round(avgPace),
    avgPaceFormatted: formatPace(Math.round(avgPace)),
    avgHr: Math.round(avgHr),
    trainingDays: aggregatedData.length,
    activitiesCount
  }
}

/**
 * 获取最近 N 天的数据
 * @param {Array} aggregatedData - 聚合后的数据
 * @param {number} days - 天数
 * @returns {Array}
 */
export function getRecentDays(aggregatedData, days) {
  const sorted = [...aggregatedData].sort((a, b) => b.date - a.date)
  return sorted.slice(0, days).reverse()
}

/**
 * 生成图表所需的数据格式
 * @param {Array} aggregatedData - 聚合后的数据
 * @param {string} field - 要提取的字段
 * @returns {Object} { dates: [], values: [] }
 */
export function prepareChartData(aggregatedData, field) {
  const sorted = [...aggregatedData].sort((a, b) => a.date - b.date)
  
  return {
    dates: sorted.map(d => d.dateFormatted),
    values: sorted.map(d => d[field])
  }
}
