# COROS Analyze Hub

基于 Vue 3 + Vite + Naive UI 构建的跑步训练数据分析看板，采用苹果风格的简洁 UI 设计。

![Vue](https://img.shields.io/badge/Vue-3.4-42b883?style=flat-square&logo=vue.js)
![Vite](https://img.shields.io/badge/Vite-5.1-646cff?style=flat-square&logo=vite)
![Naive UI](https://img.shields.io/badge/Naive_UI-2.38-18a058?style=flat-square)
![ECharts](https://img.shields.io/badge/ECharts-5.5-aa344d?style=flat-square&logo=apache-echarts)

## ✨ 功能特性

| 功能 | 说明 |
|------|------|
| 📊 **数据可视化** | ECharts 图表展示训练负荷、每日跑量、周跑量趋势 |
| 📅 **训练日历** | 月度日历视图，热力图显示训练强度 |
| 🛡️ **ACWR 风险评估** | 急慢性负荷比计算，圆环图可视化展示受伤风险 |
| 🏆 **个人记录** | 近 28 天最远距离、最高负荷、最快配速等 |
| 📋 **训练列表** | 最近训练活动详情 |
| 🤖 **AI 训练计划** | 集成通义千问，生成 4 周微周期训练计划 |
| 🎨 **Apple 风格** | 简洁现代的浅色主题设计 |

## 🛠️ 技术栈

| 类型 | 技术 |
|------|------|
| 框架 | Vue 3 (Composition API + `<script setup>`) |
| 构建 | Vite 5 |
| UI 库 | Naive UI |
| 图表 | ECharts + vue-echarts |
| AI | 阿里云通义千问 API |
| 日期 | date-fns |
| 图标 | @vicons/ionicons5 + 自定义 SVG |

## 📁 项目结构

```
coros-analyze-hub/
├── coros-activities-scraper/       # Python 爬虫脚本
│   ├── coros-activities-scraper.py
│   ├── coros-activities-scraper-by-ui.py
│   └── requirements.txt
├── public/
│   ├── activities_data.json        # 训练数据
│   └── favicon.svg                 # 网站图标
├── src/
│   ├── assets/
│   │   └── main.css                # 全局样式 (Apple 风格)
│   ├── components/
│   │   ├── HeaderNav.vue           # 顶部导航
│   │   ├── StatsOverview.vue       # 统计概览 (近28天)
│   │   ├── ActivityHeatmap.vue     # 训练日历热力图
│   │   ├── WeeklyDistanceChart.vue # 周跑量趋势
│   │   ├── TrainingLoadChart.vue   # 训练负荷图表
│   │   ├── DailyDistanceChart.vue  # 每日跑量图表
│   │   ├── ACWRCard.vue            # ACWR 风险评估
│   │   ├── PersonalRecords.vue     # 个人记录 (近28天)
│   │   ├── RecentActivities.vue    # 最近训练列表
│   │   └── AITrainingPlan.vue      # AI 训练计划 (4周微周期)
│   ├── composables/
│   │   └── useTrainingData.js      # 训练数据管理 (单例模式)
│   ├── utils/
│   │   └── dataProcessor.js        # 数据处理工具
│   ├── App.vue
│   └── main.js
├── .env.local                      # 环境变量 (API Key，不提交)
├── .gitignore
├── index.html
├── package.json
└── vite.config.js
```

## 🚀 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 配置 AI（可选）

创建 `.env.local` 文件配置通义千问 API Key：

```bash
# 通义千问 API Key
# 获取地址：https://dashscope.console.aliyun.com/
VITE_QWEN_API_KEY=sk-xxxxxxxx
```

### 3. 启动开发服务器

```bash
npm run dev
```

访问 http://localhost:5173

### 4. 构建生产版本

```bash
npm run build
npm run preview  # 预览构建结果
```

## 📊 数据格式

`public/activities_data.json` 数据结构：

```json
{
  "date": 20260105,         // 日期 YYYYMMDD
  "name": "跑步",           // 活动名称
  "distance": 8025.21,      // 距离（米）
  "duration": 2916,         // 时长（秒）
  "pace": 286,              // 配速（秒/公里）
  "avg_hr": 169,            // 平均心率
  "training_load": 105      // 训练负荷
}
```

### 数据获取

使用 `coros-activities-scraper/` 目录下的 Python 脚本从 COROS 官网抓取训练数据：

```bash
cd coros-activities-scraper
pip install -r requirements.txt
python coros-activities-scraper.py
```

## 🛡️ ACWR 计算公式

ACWR（Acute:Chronic Workload Ratio）用于评估训练负荷变化与受伤风险：

```
急性负荷 = 近 7 天 training_load 总和
慢性负荷 = 近 28 天 training_load 总和 ÷ 4
ACWR = 急性负荷 ÷ 慢性负荷
```

**风险等级划分：**

| ACWR | 风险等级 | 颜色 | 说明 |
|------|---------|------|------|
| ≤ 0.8 | 低风险 | 🟢 绿色 | 训练量偏保守 |
| 0.8 ~ 1.0 | 适中 | 🟢 绿色 | 训练状态良好 |
| 1.0 ~ 1.3 | 中等 | 🟡 黄色 | 负荷稳步增长 |
| 1.3 ~ 1.5 | 较高 | 🟠 橙色 | 负荷增长较快 |
| > 1.5 | 高风险 | 🔴 红色 | 建议减量恢复 |

> 建议范围：0.8 ~ 1.3

## 🤖 AI 训练计划

集成阿里云通义千问 API，根据以下数据生成 **4 周微周期训练计划**：

- 近期训练数据和跑量趋势
- ACWR 受伤风险指标
- 目标成绩和当前训练阶段

**计划特点：**

- 📆 日历视图展示每日训练安排
- 🎨 颜色编码：轻松跑（绿）、间歇/节奏（橙）、长距离（蓝）、休息（灰）
- 📈 渐进式负荷增加，第 4 周减量恢复
- 📝 每周训练目标和周跑量建议

**配置步骤：**

1. 获取 API Key：https://dashscope.console.aliyun.com/
2. 创建 `.env.local` 文件并添加：
   ```
   VITE_QWEN_API_KEY=sk-xxxxxxxx
   ```
3. 重启开发服务器

## 🎨 主题定制

修改 `src/assets/main.css` 中的 CSS 变量：

```css
:root {
  /* 主色调 */
  --blue: #0071e3;
  --green: #34c759;
  --orange: #ff9500;
  --red: #ff3b30;
  
  /* 文字颜色 */
  --text-primary: #1d1d1f;
  --text-secondary: #6e6e73;
  
  /* 背景 */
  --bg-primary: #ffffff;
  --bg-secondary: #f5f5f7;
  
  /* 圆角 */
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 20px;
}
```

## 📝 扩展开发

### 添加新图表组件

1. 在 `src/components/` 创建新的 Vue 组件
2. 导入 ECharts 所需模块
3. 使用 `useTrainingData()` 获取数据
4. 在 `App.vue` 中引入并放置

### 添加新统计指标

1. 在 `src/utils/dataProcessor.js` 添加计算函数
2. 在 `useTrainingData.js` 添加计算属性
3. 在相应组件中使用

## 📄 License

MIT
