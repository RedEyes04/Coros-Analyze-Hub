#!/usr/bin/env python3
import json
import requests
from pathlib import Path

BASE_DIR = Path(__file__).parent
TOKEN_FILE = BASE_DIR / "token.txt"
OUT_FILE = BASE_DIR / "activities_data.json"

API_URL = "https://t.coros.com/activity/query"

def load_token():
    raw = TOKEN_FILE.read_text(encoding="utf-8").strip()

    if not raw:
        raise RuntimeError("❌ token.txt 为空")

    if "\n" in raw or " " in raw:
        raise RuntimeError("❌ token.txt 必须只有一行")

    if raw.startswith("CPL-coros-token="):
        return raw.split("=", 1)[1]

    raise RuntimeError("❌ token.txt 格式错误")

def fetch_data(token: str):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://t.coros.com",
        "Referer": "https://t.coros.com/",
        # 🔑 核心鉴权
        "Authorization": f"Bearer {token}",
        "Cookie": f"CPL-coros-token={token}",
    }

    payload = {
        "pageNumber": 1,
        "pageSize": 20
    }

    resp = requests.post(API_URL, json=payload, headers=headers, timeout=15)

    if resp.status_code == 401:
        raise RuntimeError("❌ 401：token 未登录或已失效")
    if resp.status_code == 403:
        raise RuntimeError("❌ 403：token 权限不足（需重新获取）")
    if resp.status_code == 404:
        raise RuntimeError("❌ 404：接口路径变更（需重新抓包）")

    resp.raise_for_status()
    return resp.json()

def main():
    print("📡 开始抓取 COROS 活动数据")

    token = load_token()
    data = fetch_data(token)

    OUT_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"✅ 抓取完成：{OUT_FILE}")

if __name__ == "__main__":
    main()