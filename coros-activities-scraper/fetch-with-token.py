#!/usr/bin/env python3
"""
服务器端 COROS 数据抓取脚本

目录结构：
/www/wwwroot/coros.redeyes.top/
├── token.txt
├── fetch.py
└── activities_data.json
"""

import json
import requests
from pathlib import Path

BASE_DIR = Path(__file__).parent
TOKEN_FILE = BASE_DIR / "token.txt"
OUTPUT_FILE = BASE_DIR / "activities_data.json"

API_URL = "https://t.coros.com/activity/query"  # 示例


def read_token():
    return TOKEN_FILE.read_text().splitlines()[0].strip()


def fetch_data(token: str):
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "Mozilla/5.0"
    }

    resp = requests.get(API_URL, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()


def main():
    token = read_token()
    data = fetch_data(token)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("activities_data.json 已生成")


if __name__ == "__main__":
    main()