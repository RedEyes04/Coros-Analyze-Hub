# COROS Activities Scraper

从 COROS 官网抓取跑步训练数据的 Python 脚本集合。

## 📁 脚本说明

| 脚本 | 用途 | 运行环境 |
|------|------|----------|
| `get-token.py` | 本地登录获取 token，自动推送到 GitHub | 本地电脑 |
| `fetch-with-token.py` | 根据 token 调用 API 抓取数据 | 服务器/本地 |
| `coros-activities-scraper.py` | 一体化脚本：登录 + 抓取 | 本地电脑 |
| `coros-activities-scraper-by-ui.py` | 自动登录版（CI 用，需配置账密） | CI/本地 |（弃用）

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
playwright install chromium
```

### 方式一：一体化抓取（推荐新手）

```bash
python coros-activities-scraper.py
```

会弹出浏览器 → 手动登录 → 自动抓取 → 保存数据

### 方式二：自动化流程

#### Step 1: 本地获取 Token

```bash
python get-token.py
```

会：
1. 弹出浏览器让你登录
2. 检测到登录成功后获取 token
3. 保存到 `token.txt`
4. 自动 git commit & push

#### Step 2: GitHub Actions 自动触发

推送后，GitHub Actions 会自动：
1. rsync token 文件到你的服务器
2. 在服务器执行 `fetch-with-token.py`
3. 将抓取的数据 push 回仓库

## ⚙️ GitHub Actions 配置

需要在仓库 Settings → Secrets and variables → Actions 中配置：

| Secret | 说明 | 示例 |
|--------|------|------|
| `SERVER_HOST` | 服务器地址 | `192.168.1.100` 或 `coros.redeyes.top` |
| `SERVER_PASSWORD` | 服务器 root 密码 | `your-password` |

服务器项目路径已固定为：`/www/wwwroot/coros.redeyes.top/`

## 📊 输出格式

`activities_data.json` 结构：

```json
[
  {
    "date": 20260105,
    "name": "跑步",
    "distance": 8025.21,
    "duration": 2916,
    "pace": 286,
    "avg_hr": 169,
    "training_load": 105
  }
]
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `date` | int | 日期 YYYYMMDD |
| `name` | string | 活动名称 |
| `distance` | float | 距离（米） |
| `duration` | int | 时长（秒） |
| `pace` | int | 配速（秒/公里） |
| `avg_hr` | int | 平均心率 |
| `training_load` | int | 训练负荷 |

## ⚠️ 安全提示

1. **Token 有效期**：COROS token 通常有效期较长，但建议定期更新
2. **私有仓库**：如果 token.txt 会提交到仓库，建议使用私有仓库
3. **环境变量**：生产环境建议通过环境变量或 Secrets 传递 token

## 🔧 命令行参数

`fetch-with-token.py` 支持以下参数：

```bash
python fetch-with-token.py --help

# 指定 token
python fetch-with-token.py --token "your-token-here"

# 指定抓取页数（每页 20 条）
python fetch-with-token.py --pages 5

# 指定输出文件
python fetch-with-token.py --output ./data/activities.json
```

## 📝 License

MIT
