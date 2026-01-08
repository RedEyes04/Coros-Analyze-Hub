# COROS Analyze Hub

COROS 手表跑步数据的抓取和可视化工具。

## 项目组成

```
coros-analyze-hub/
├── coros-activities-scraper/    # Python 爬虫
│   ├── get-token.py             # 本地获取登录 cookies
│   ├── fetch.py                 # 服务器抓取数据
│   └── coros-activities-scraper.py  # 一体化脚本
│
├── .github/workflows/coros.yml  # GitHub Actions 自动化
│
└── src/                         # Vue 前端
    └── components/              # 10 个图表组件
```

## 数据流

```
本地登录 COROS → 保存 cookies → push 到 GitHub
                                      ↓
                              GitHub Actions 触发
                                      ↓
                              服务器执行抓取脚本
                                      ↓
                    https://coros.redeyes.top/activities_data.json
                                      ↓
                                前端获取展示
```

## 使用方法

### 1. 抓取数据

```bash
cd coros-activities-scraper
pip install -r requirements.txt
playwright install chromium

# 方式一：本地一体化抓取
python coros-activities-scraper.py

# 方式二：自动化流程（需配置服务器）
python get-token.py
```

### 2. 启动前端

```bash
npm install
npm run dev
```

访问 http://localhost:5173

### 3. GitHub Actions 配置

需要在仓库 Secrets 中添加：

- `SERVER_HOST` - 服务器地址
- `SERVER_PASSWORD` - 服务器密码

## 数据格式

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

## 前端功能

- 训练日历热力图
- 训练负荷趋势图
- 每日/每周跑量图表
- ACWR 受伤风险评估
- 个人记录（28天内）
- 最近训练列表
- AI 训练计划生成（需配置通义千问 API）

## AI 配置

创建 `.env.local`：

```
VITE_QWEN_API_KEY=sk-xxx
```

## 技术栈

- 爬虫：Python + Playwright
- 前端：Vue 3 + Vite + Naive UI + ECharts
- 自动化：GitHub Actions + rsync

## License

MIT
