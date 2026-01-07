#!/usr/bin/env python3
import json
import requests
from pathlib import Path

TOKEN_FILE = Path("token.txt")
OUTPUT_FILE = Path("activities_data.json")

API_URL = "https://t.coros.com/activity/query"

def read_token():
    if not TOKEN_FILE.exists():
        raise RuntimeError("❌ token.txt 不存在")

    with open(TOKEN_FILE) as f:
        for line in f:
            if line.startswith("CPL-coros-token="):
                return line.strip().split("=", 1)[1]

    raise RuntimeError("❌ token.txt 中未找到有效 token")


def fetch_data(token: str):
    headers = {
        "Authorization": token,
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json"
    }

    payload = {
        "page": 1,
        "size": 20
    }

    resp = requests.post(API_URL, json=payload, headers=headers, timeout=15)

    if resp.status_code == 401:
        raise RuntimeError("❌ 401：token 已失效，请重新登录获取")
    if resp.status_code == 403:
        raise RuntimeError("❌ 403：token 权限不足")
    if resp.status_code == 404:
        raise RuntimeError("❌ 404：COROS 接口地址已变动（需要更新 fetch.py）")

    resp.raise_for_status()

    try:
        data = resp.json()
    except Exception:
        raise RuntimeError("❌ 返回内容不是 JSON，接口可能已调整")

    return data


def main():
    print("📡 开始抓取 COROS 活动数据")

    token = read_token()
    data = fetch_data(token)

    if not data:
        raise RuntimeError("⚠️ 接口返回为空数据")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ 抓取完成，已生成 {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    main()