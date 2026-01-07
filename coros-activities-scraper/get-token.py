#!/usr/bin/env python3
import time
import subprocess
from datetime import datetime
from playwright.sync_api import sync_playwright

TOKEN_FILE = "coros-activities-scraper/token.txt"
COMMIT_MSG = "chore: update COROS token"

def get_token():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://t.coros.com/login")
        print("请在浏览器中完成 COROS 登录（2 分钟内）")

        token = None
        for _ in range(60):
            time.sleep(2)
            for c in context.cookies():
                if c["name"] == "CPL-coros-token":
                    token = c["value"]
                    break
            if token:
                break

        browser.close()
        return token


def save_token(token: str):
    content = (
        f"CPL-coros-token={token}\n"
        f"# updated_at: {datetime.now()}\n"
        f"# source: local-browser\n"
    )
    with open(TOKEN_FILE, "w") as f:
        f.write(content)


def git_commit_push():
    diff = subprocess.run(
        ["git", "status", "--porcelain", TOKEN_FILE],
        capture_output=True,
        text=True
    ).stdout.strip()

    if not diff:
        print("⚠️ token 文件未发生变化（Git 认为相同）")
        print("👉 已自动更新时间，仍可触发 workflow")
    
    subprocess.run(["git", "add", TOKEN_FILE], check=True)
    subprocess.run(["git", "commit", "-m", COMMIT_MSG], check=True)
    subprocess.run(["git", "push"], check=True)


def main():
    print("🏃 COROS Token 获取工具\n")

    token = get_token()
    if not token:
        print("❌ 未检测到 token，请确认是否登录成功")
        return

    print(f"✅ 获取 token 成功：{token[:20]}...{token[-8:]}")
    save_token(token)

    print("📤 正在推送到 GitHub...")
    git_commit_push()

    print("\n🎉 完成：GitHub Actions 将自动同步并抓取数据")


if __name__ == "__main__":
    main()