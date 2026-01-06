# COROS Analyze Hub

一站式 COROS 跑步训练数据分析平台，包含数据抓取、自动化同步和可视化分析三大模块。

![Vue](https://img.shields.io/badge/Vue-3.4-42b883?style=flat-square&logo=vue.js)
![Vite](https://img.shields.io/badge/Vite-5.1-646cff?style=flat-square&logo=vite)
![Python](https://img.shields.io/badge/Python-3.10+-3776ab?style=flat-square&logo=python)
![Playwright](https://img.shields.io/badge/Playwright-1.40+-45ba4b?style=flat-square&logo=playwright)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white)

## 🎯 项目简介

本项目帮助 COROS 手表用户更好地分析训练数据，由三部分组成：

1. **数据抓取** - Python + Playwright 自动化脚本，从 COROS 官网抓取训练记录
2. **自动化同步** - GitHub Actions + rsync，实现本地登录 → 服务器抓取 → 数据更新
3. **数据分析** - Vue 3 前端看板，可视化展示训练数据和 AI 训练建议

## ✨ 功能特性

### 📥 数据抓取 (Python)

| 功能 | 说明 |
|------|------|
| 🔐 手动登录模式 | 弹出浏览器，用户手动登录后自动抓取 |
| 🔑 Token 分离模式 | 本地获取 token，服务器端执行抓取 |
| 📄 JSON 导出 | 输出标准化的训练数据文件 |
| 🔄 增量抓取 | 支持配置抓取页数，获取最近训练记录 |

### 🔄 自动化流程 (GitHub Actions)

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│ 本地登录  │────▶│  GitHub  │────▶│  Actions │────▶│  服务器   │
│ 获取token │     │   仓库    │     │  rsync   │     │  抓取数据 │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
```

### 📊 数据分析 (Vue)

| 功能 | 说明 |
|------|------|
| 📈 趋势图表 | 训练负荷、每日跑量、周跑量折线/柱状图 |
| 📅 训练日历 | 月度日历热力图，显示训练强度分布 |
| 🛡️ ACWR 评估 | 急慢性负荷比计算，圆环图展示受伤风险 |
| 🏆 个人记录 | 近 28 天最远距离、最高负荷、最快配速 |
| 📋 训练列表 | 最近训练活动详情展示 |
| 🤖 AI 训练计划 | 通义千问生成 4 周微周期训练计划 |
| 🎨 Apple 风格 | 简洁现代的浅色主题 UI |

## 🛠️ 技术栈

| 模块 | 技术 |
|------|------|
| **数据抓取** | Python 3.10+、Playwright、Requests |
| **自动化** | GitHub Actions、rsync、SSH |
| **前端框架** | Vue 3 (Composition API + `<script setup>`) |
| **构建工具** | Vite 5 |
| **UI 组件** | Naive UI |
| **图表** | ECharts + vue-echarts |
| **AI** | 阿里云通义千问 API |

## 📁 项目结构

```
coros-analyze-hub/
├── .github/
│   └── workflows/
│       └── sync-and-fetch.yml      # 🔄 GitHub Actions 自动化
│
├── coros-activities-scraper/       # 🐍 Python 数据抓取模块
│   ├── get-token.py                # 本地获取 token + git push
│   ├── fetch-with-token.py         # 服务器端抓取脚本
│   ├── coros-activities-scraper.py # 一体化脚本（登录+抓取）
│   ├── token.txt                   # Token 文件（触发 Actions）
│   └── requirements.txt
│
├── public/                         # 📂 静态资源
│   ├── activities_data.json        # 训练数据
│   └── favicon.svg
│
├── src/                            # 🎨 Vue 前端源码
│   ├── components/                 # 10 个可视化组件
│   ├── composables/                # 数据管理逻辑
│   ├── utils/                      # 工具函数
│   └── ...
│
├── .env.local                      # 环境变量（API Key）
├── index.html
├── package.json
└── vite.config.js
```

## 🚀 快速开始

### 方式一：手动抓取（推荐新手）

```bash
# 1. 进入爬虫目录
cd coros-activities-scraper

# 2. 安装依赖
pip install -r requirements.txt
playwright install chromium

# 3. 运行一体化脚本
python coros-activities-scraper.py
```

### 方式二：自动化流程

#### Step 1: 配置 GitHub Secrets

在仓库 Settings → Secrets → Actions 中添加：

| Secret | 说明 |
|--------|------|
| `SSH_HOST` | 服务器地址 |
| `SSH_USER` | SSH 用户名 |
| `SSH_PRIVATE_KEY` | SSH 私钥 |
| `SSH_PORT` | SSH 端口（默认 22） |
| `REMOTE_PATH` | 服务器项目路径 |

#### Step 2: 服务器准备

```bash
# 在服务器上克隆项目
git clone https://github.com/your-username/coros-analyze-hub.git
cd coros-analyze-hub/coros-activities-scraper

# 安装 Python 依赖
pip install -r requirements.txt
```

#### Step 3: 本地触发同步

```bash
cd coros-activities-scraper
python get-token.py
```

脚本会：
1. 弹出浏览器让你登录 COROS
2. 获取 token 并保存
3. 自动 git push 到 GitHub
4. 触发 Actions → 服务器抓取 → 数据更新

### 启动分析看板

```bash
# 项目根目录
npm install
npm run dev
```

访问 http://localhost:5173

### 配置 AI（可选）

创建 `.env.local`：

```bash
VITE_QWEN_API_KEY=sk-xxxxxxxx
```

## 📊 数据格式

```json
{
  "date": 20260105,
  "name": "跑步",
  "distance": 8025.21,
  "duration": 2916,
  "pace": 286,
  "avg_hr": 169,
  "training_load": 105
}
```

## 🛡️ ACWR 计算

```
急性负荷 = 近 7 天 training_load 总和
慢性负荷 = 近 28 天 training_load 总和 ÷ 4
ACWR = 急性负荷 ÷ 慢性负荷
```

| ACWR | 风险 | 说明 |
|------|------|------|
| ≤ 0.8 | 🟢 低 | 训练保守 |
| 0.8 ~ 1.3 | 🟢 适中 | 状态良好 |
| 1.3 ~ 1.5 | 🟠 较高 | 增长较快 |
| > 1.5 | 🔴 高 | 建议减量 |

## 🤖 AI 训练计划

通义千问根据训练数据生成 4 周微周期计划：

- 📆 日历视图展示每日安排
- 🎨 颜色编码（绿-轻松跑 / 橙-间歇 / 蓝-长距离 / 灰-休息）
- 📈 渐进负荷，第 4 周减量恢复

## 📄 License

MIT

---

<p align="center">
  <sub>Built with ❤️ for COROS runners🏃</sub>
</p>
