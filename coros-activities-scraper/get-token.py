#!/usr/bin/env python3
import time
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).parent
TOKEN_FILE = BASE_DIR / "token.txt"
COMMIT_MSG = "chore: update COROS token"

def get_token_from_browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # 1️⃣ 打开登录页
        page.goto("https://t.coros.com/login")
        print("👉 请在浏览器中完成 COROS 登录（2 分钟内）")

        token = None
        for _ in range(60):
            time.sleep(2)
            for c in context.cookies():
                if c["name"] == "CPL-coros-token":
                    token = c["value"]
                    break
            if token:
                break

        if not token:
            browser.close()
            return None

        # 2️⃣ 关键一步：访问 activity 页面，补全权限
        page.goto("https://t.coros.com/activity")
        time.sleep(5)

        browser.close()
        return token

def save_token(token: str):
    TOKEN_FILE.write_text(
        f"CPL-coros-token={token}",
        encoding="utf-8"
    )
    print(f"✅ token 已保存到 {TOKEN_FILE}")

def git_commit_push():
    subprocess.run(["git", "add", str(TOKEN_FILE)], check=True)
    subprocess.run(["git", "commit", "-m", COMMIT_MSG], check=True)
    subprocess.run(["git", "push"], check=True)

def main():
    print("🏃 COROS Token 获取工具\n")

    token = get_token_from_browser()
    if not token:
        print("❌ 未获取到 token，请确认是否登录成功")
        return

    print(f"✅ 获取 token 成功：{token[:20]}...{token[-8:]}")
    save_token(token)

    print("📤 推送到 GitHub（触发 Actions）...")
    git_commit_push()

    print("\n🎉 完成：GitHub Actions 将自动同步并抓取数据")

if __name__ == "__main__":
    main()