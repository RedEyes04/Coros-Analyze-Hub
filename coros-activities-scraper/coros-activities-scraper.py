import json
import time
from playwright.sync_api import sync_playwright

API_URL = "https://teamcnapi.coros.com/activity/query"
OUTPUT_FILE = "../public/activities_data.json"
MAX_PAGE = 3   # 抓最近 3 页

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://t.coros.com/login")
        print("请在弹出的浏览器中登录 COROS...")

        # 等待 token
        token = None
        for _ in range(60):
            time.sleep(2)
            for c in context.cookies():
                if c["name"] == "CPL-coros-token":
                    token = c["value"]
                    break
            if token:
                print("检测到登录完成，获取到 token！")
                break

        if not token:
            print("未检测到 token，请检查是否登录成功")
            browser.close()
            return

        print(f"获取到 token: {token}")

        headers = {
            "accept": "application/json, text/plain, */*",
            "accesstoken": token,
            "origin": "https://t.coros.com",
            "referer": "https://t.coros.com/",
            "user-agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
            ),
        }

        all_activities = []

        # 抓取最近 3 页
        for page_num in range(1, MAX_PAGE + 1):
            print(f"抓取第 {page_num} 页...")
            params = {
                "size": 20,
                "pageNumber": page_num,
                "modeList": ""
            }

            response = page.request.get(API_URL, params=params, headers=headers)

            try:
                data = response.json()
            except Exception as e:
                print("解析 JSON 失败:", e)
                break

            activities = data.get("data", {}).get("dataList", [])
            if not activities:
                print("该页无数据，停止抓取")
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

            time.sleep(0.5)  # 防止请求过快

        if not all_activities:
            print("未抓取到任何训练数据")
            browser.close()
            return

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(all_activities, f, ensure_ascii=False, indent=4)

        print(f"抓取完成，共抓到 {len(all_activities)} 条训练数据")
        print(f"已保存到 {OUTPUT_FILE}")

        input("按回车退出...")
        browser.close()

if __name__ == "__main__":
    main()