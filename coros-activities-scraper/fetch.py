#!/usr/bin/env python3
"""
COROS 数据抓取脚本（服务器端运行）

使用 cookies.json 中的完整 cookies 调用 COROS API
"""
import json
import requests
from pathlib import Path

BASE_DIR = Path(__file__).parent
COOKIES_FILE = BASE_DIR / "cookies.json"
OUT_FILE = BASE_DIR / "activities_data.json"

# COROS API（中国区）
API_URL = "https://teamcnapi.coros.com/activity/query"
MAX_PAGES = 3
PAGE_SIZE = 20


def load_cookies():
    """从 cookies.json 读取 cookies"""
    if not COOKIES_FILE.exists():
        raise RuntimeError(f"❌ {COOKIES_FILE} 不存在")
    
    cookies = json.loads(COOKIES_FILE.read_text(encoding="utf-8"))
    
    if not cookies:
        raise RuntimeError("❌ cookies.json 为空")
    
    return cookies


def cookies_to_dict(cookies: list) -> dict:
    """将 Playwright cookies 格式转换为 requests 可用的 dict"""
    return {c["name"]: c["value"] for c in cookies}


def get_token(cookies: list) -> str:
    """从 cookies 中提取 token"""
    for c in cookies:
        if c["name"] == "CPL-coros-token":
            return c["value"]
    raise RuntimeError("❌ cookies 中没有 CPL-coros-token")


def fetch_data(cookies: list):
    """调用 COROS API 抓取数据"""
    token = get_token(cookies)
    cookies_dict = cookies_to_dict(cookies)
    
    headers = {
        "accept": "application/json, text/plain, */*",
        "accesstoken": token,
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

        params = {
            "size": PAGE_SIZE,
            "pageNumber": page_num,
            "modeList": ""
        }

        # ✅ 关键：同时使用 cookies 和 headers
        resp = requests.get(
            API_URL, 
            params=params, 
            headers=headers, 
            cookies=cookies_dict,
            timeout=30
        )

        print(f"   📊 HTTP {resp.status_code}")
        
        if resp.status_code == 401:
            raise RuntimeError("❌ 401：cookies 已失效，请重新运行 get-token.py")
        if resp.status_code == 403:
            raise RuntimeError("❌ 403：权限不足，请重新运行 get-token.py")
        
        resp.raise_for_status()
        
        try:
            data = resp.json()
        except json.JSONDecodeError:
            print(f"   ⚠️ 响应不是 JSON: {resp.text[:200]}")
            break

        # 提取数据
        activities = data.get("data", {}).get("dataList", [])
        
        if not activities:
            print(f"   ℹ️ 第 {page_num} 页无数据，停止")
            if page_num == 1:
                # 第一页就没数据，打印调试信息
                print(f"   🔍 响应: {json.dumps(data, ensure_ascii=False)[:300]}")
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

    cookies = load_cookies()
    print(f"🍪 加载了 {len(cookies)} 个 cookies")
    
    token = get_token(cookies)
    print(f"🔑 Token: {token[:15]}...{token[-8:]}\n")

    activities = fetch_data(cookies)

    if not activities:
        print("\n⚠️ 未抓取到数据")
        return 1

    OUT_FILE.write_text(
        json.dumps(activities, ensure_ascii=False, indent=4),
        encoding="utf-8"
    )

    print(f"\n✅ 抓取完成：共 {len(activities)} 条，保存到 {OUT_FILE}")
    return 0


if __name__ == "__main__":
    exit(main())
