# COROS Analyze Hub - 训练数据分析看板

基于 Vue 3 + Vite + Naive UI 构建的跑步训练数据分析前端应用。

## 功能特性

- 📊 **训练数据可视化**：ECharts 图表展示训练负荷和跑量趋势
- 🛡️ **ACWR 风险评估**：急慢性负荷比计算，评估受伤风险
- 🤖 **AI 训练建议**：基于通义千问大模型生成个性化训练计划
- 🌙 **深色主题**：运动科技风格的现代 UI 设计

## 技术栈

- **框架**: Vue 3 (Composition API + `<script setup>`)
- **构建工具**: Vite 5
- **UI 组件库**: Naive UI
- **图表库**: ECharts + vue-echarts
- **图标**: @vicons/ionicons5
- **日期处理**: date-fns

## 项目结构

```
Frontend/
├── public/
│   ├── activities_data.json    # 训练数据文件
│   └── favicon.svg
├── src/
│   ├── assets/
│   │   └── main.css            # 全局样式（CSS 变量、主题）
│   ├── components/
│   │   ├── HeaderNav.vue       # 顶部导航栏
│   │   ├── StatsOverview.vue   # 统计概览卡片
│   │   ├── TrainingLoadChart.vue   # 训练负荷折线图
│   │   ├── DailyDistanceChart.vue  # 每日跑量折线图
│   │   ├── ACWRCard.vue        # ACWR 风险评估卡片
│   │   └── AITrainingPlan.vue  # AI 训练计划组件
│   ├── composables/
│   │   └── useTrainingData.js  # 训练数据 Composable
│   ├── utils/
│   │   └── dataProcessor.js    # 数据处理工具函数
│   ├── App.vue                 # 根组件
│   └── main.js                 # 入口文件
├── index.html
├── package.json
├── vite.config.js
└── README.md
```

## 快速开始

### 安装依赖

```bash
cd Frontend
npm install
```

### 启动开发服务器

```bash
npm run dev
```

访问 http://localhost:5173

### 构建生产版本

```bash
npm run build
```

## 数据格式

`activities_data.json` 数据结构：

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

## ACWR 计算逻辑

```
急性负荷 (Acute Load) = 最近 7 天 training_load 总和
慢性负荷 (Chronic Load) = 最近 28 天 training_load 总和 ÷ 4
ACWR = Acute Load / Chronic Load
```

风险等级划分：
- ≤ 0.8 → 低风险（训练量偏保守）
- 0.8 ~ 1.0 → 适中（训练状态良好）
- 1.0 ~ 1.3 → 中等（负荷稳步增长）
- 1.3 ~ 1.5 → 较高（负荷增长较快）
- > 1.5 → 高风险（建议减量）

## AI 接口集成

项目预留了通义千问 API 调用接口。实际部署时，建议：

1. **后端代理**：在后端实现 API 代理，保护 API Key
2. **创建 `/api/ai/training-plan` 接口**：

```javascript
// 后端示例（Node.js）
app.post('/api/ai/training-plan', async (req, res) => {
  const response = await fetch('https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.DASHSCOPE_API_KEY}`
    },
    body: JSON.stringify({
      model: 'qwen-turbo',
      input: {
        messages: req.body.messages
      }
    })
  });
  
  const data = await response.json();
  res.json(data);
});
```

## 扩展开发

### 添加新图表

1. 在 `src/components/` 创建新组件
2. 导入 ECharts 所需模块
3. 在 `App.vue` 中引入并放置

### 添加新统计卡片

1. 在 `useTrainingData.js` 添加计算属性
2. 在 `StatsOverview.vue` 的 `statsCards` 数组中添加配置

### 自定义主题

修改 `src/assets/main.css` 中的 CSS 变量：

```css
:root {
  --primary-100: #00f5ff;  /* 主色调 */
  --accent-100: #ff00ff;   /* 强调色 */
  --bg-primary: #0a0e17;   /* 背景色 */
  /* ... */
}
```

## License

MIT
