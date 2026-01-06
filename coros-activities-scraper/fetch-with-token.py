#!/usr/bin/env python3
"""
COROS 数据抓取脚本（服务器端运行）

功能：
1. 从 token.txt 读取 COROS token
2. 调用 COROS API 抓取训练数据
3. 保存到 activities_data.json

使用方式：
    python fetch-with-token.py [--token TOKEN] [--pages 3] [--output OUTPUT_FILE]

参数：
    --token   直接传入 token（可选，默认从 token.txt 读取）
    --pages   抓取页数（可选，默认 3 页 = 60 条）
    --output  输出文件路径（可选，默认 ../public/activities_data.json）
"""

import os
import json
import argparse
import requests
from datetime import datetime

# 配置
API_URL = "https://teamcnapi.coros.com/activity/query"
DEFAULT_TOKEN_FILE = "token.txt"
# 默认输出路径（相对于脚本所在目录）
# 本地: ../public/activities_data.json
# 服务器: /www/wwwroot/coros.redeyes.top/public/activities_data.json
DEFAULT_OUTPUT_FILE = "../public/activities_data.json"
DEFAULT_PAGES = 3
PAGE_SIZE = 20

# 请求头
HEADERS_TEMPLATE = {
    "accept": "application/json, text/plain, */*",
    "origin": "https://t.coros.com",
    "referer": "https://t.coros.com/",
    "user-agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
}


def read_token(token_file: str) -> str:
    """从文件读取 token（忽略注释行）"""
    if not os.path.exists(token_file):
        raise FileNotFoundError(f"Token 文件不存在: {token_file}")
    
    with open(token_file, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                return line
    
    raise ValueError("Token 文件中没有有效的 token")


def fetch_activities(token: str, max_pages: int) -> list:
    """通过 API 抓取训练数据"""
    headers = {**HEADERS_TEMPLATE, "accesstoken": token}
    all_activities = []
    
    for page_num in range(1, max_pages + 1):
        print(f"📥 抓取第 {page_num}/{max_pages} 页...")
        
        params = {
            "size": PAGE_SIZE,
            "pageNumber": page_num,
            "modeList": ""
        }
        
        try:
            response = requests.get(API_URL, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            print(f"❌ 请求失败: {e}")
            break
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析失败: {e}")
            break
        
        # 检查 API 响应
        if data.get("code") != "success":
            print(f"❌ API 返回错误: {data.get('message', 'Unknown error')}")
            if "token" in str(data).lower():
                print("💡 提示：Token 可能已过期，请重新运行 get-token.py")
            break
        
        activities = data.get("data", {}).get("dataList", [])
        if not activities:
            print(f"ℹ️  第 {page_num} 页无数据，停止抓取")
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
        
        print(f"   ✅ 获取 {len(activities)} 条记录")
    
    return all_activities


def save_activities(activities: list, output_file: str):
    """保存训练数据到 JSON 文件"""
    # 确保输出目录存在
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(activities, f, ensure_ascii=False, indent=4)
    
    print(f"✅ 数据已保存到 {output_file}")


def main():
    parser = argparse.ArgumentParser(description="COROS 训练数据抓取脚本")
    parser.add_argument("--token", help="COROS token（不指定则从 token.txt 读取）")
    parser.add_argument("--pages", type=int, default=DEFAULT_PAGES, help=f"抓取页数（默认 {DEFAULT_PAGES}）")
    parser.add_argument("--output", default=DEFAULT_OUTPUT_FILE, help=f"输出文件路径（默认 {DEFAULT_OUTPUT_FILE}）")
    args = parser.parse_args()
    
    print("\n🏃 COROS 数据抓取工具\n")
    print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 40)
    
    # 获取 token
    try:
        if args.token:
            token = args.token
            print("📝 使用命令行传入的 token")
        else:
            token = read_token(DEFAULT_TOKEN_FILE)
            print(f"📝 从 {DEFAULT_TOKEN_FILE} 读取 token")
        
        print(f"   Token: {token[:20]}...{token[-10:]}")
    except (FileNotFoundError, ValueError) as e:
        print(f"❌ {e}")
        return 1
    
    print("-" * 40)
    
    # 抓取数据
    activities = fetch_activities(token, args.pages)
    
    if not activities:
        print("\n❌ 未抓取到任何数据")
        return 1
    
    print("-" * 40)
    print(f"📊 共抓取 {len(activities)} 条训练记录")
    
    # 保存数据
    save_activities(activities, args.output)
    
    print("-" * 40)
    print(f"⏰ 完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎉 抓取完成！\n")
    
    return 0


if __name__ == "__main__":
    exit(main())
