# COROS 数据抓取

## 脚本说明

| 脚本 | 用途 |
|------|------|
| `get-token.py` | 本地登录，保存 cookies，push 触发 Actions |
| `fetch.py` | 服务器端抓取数据 |
| `coros-activities-scraper.py` | 本地一体化抓取 |

## 安装

```bash
pip install -r requirements.txt
playwright install chromium
```

## 使用

```bash
# 方式一：本地一体化
python coros-activities-scraper.py

# 方式二：自动化流程
python get-token.py
```

## 输出

`activities_data.json` - 训练数据 JSON 文件
