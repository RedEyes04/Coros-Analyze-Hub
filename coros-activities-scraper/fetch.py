#!/usr/bin/env python3
"""
COROS 数据抓取脚本（服务器端运行）
根据 token.txt 中的 token 调用 COROS API 抓取训练数据
"""
import json
import requests
from pathlib import Path

BASE_DIR = Path(__file__).parent
TOKEN_FILE = BASE_DIR / "token.txt"
OUT_FILE = BASE_DIR / "activities_data.json"

# ✅ 正确的 API 地址（中国区）
API_URL = "https://teamcnapi.coros.com/activity/query"
MAX_PAGES = 3
PAGE_SIZE = 20


def load_token():
    """从 token.txt 读取 token"""
    raw = TOKEN_FILE.read_text(encoding="utf-8").strip()

    if not raw:
        raise RuntimeError("❌ token.txt 为空")

    # 支持两种格式：
    # 1. CPL-coros-token=xxxx
    # 2. 纯 token
    if "=" in raw:
        return raw.split("=", 1)[1].strip()
    
    return raw


def fetch_data(token: str):
    """调用 COROS API 抓取数据"""
    # ✅ 正确的请求头（参考原始抓取脚本）
    headers = {
        "accept": "application/json, text/plain, */*",
        "accesstoken": token,  # ✅ 关键：使用 accesstoken header
        "origin": "https://t.coros.com",
        "referer": "https://t.coros.com/",
        "user-agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
    }

    all_activities = []

    for page_num in range(1, MAX_PAGES + 1):
        print(f"📥 抓取第 {page_num}/{MAX_PAGES} 页...")

        # ✅ 正确的请求方式：GET + params
        params = {
            "size": PAGE_SIZE,
            "pageNumber": page_num,
            "modeList": ""
        }

        resp = requests.get(API_URL, params=params, headers=headers, timeout=30)

        if resp.status_code == 401:
            raise RuntimeError("❌ 401：token 未登录或已失效")
        if resp.status_code == 403:
            raise RuntimeError("❌ 403：token 权限不足（需重新获取 token）")
        
        resp.raise_for_status()
        data = resp.json()

        # 检查返回结果
        activities = data.get("data", {}).get("dataList", [])
        if not activities:
            print(f"   ℹ️ 第 {page_num} 页无数据，停止")
            break

        for a in activities:
            all_activities.append({
                "date": a.get("date"),
                "name": a.get("name"),
                "distance": a.get("distance"),
                "duration": a.get("totalTime"),
                "pace": a.get("adjustedPace"),
                "avg_hr": a.get("avgHr"),
                "training_load": a.get("trainingLoad")
            })

        print(f"   ✅ 获取 {len(activities)} 条")

    return all_activities


def main():
    print("📡 开始抓取 COROS 活动数据\n")

    token = load_token()
    print(f"🔑 Token: {token[:15]}...{token[-8:]}\n")

    activities = fetch_data(token)

    if not activities:
        raise RuntimeError("❌ 未抓取到任何数据")

    OUT_FILE.write_text(
        json.dumps(activities, ensure_ascii=False, indent=4),
        encoding="utf-8"
    )

    print(f"\n✅ 抓取完成：共 {len(activities)} 条，保存到 {OUT_FILE}")


if __name__ == "__main__":
    main()
