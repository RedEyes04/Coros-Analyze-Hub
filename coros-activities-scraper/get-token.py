#!/usr/bin/env python3
"""
COROS Token 获取脚本（本地运行）

职责：
1. 打开浏览器手动登录 COROS
2. 获取 CPL-coros-token
3. 写入 token.txt
4. git commit & push

只做这四件事
"""

import time
import subprocess
from playwright.sync_api import sync_playwright
from datetime import datetime

TOKEN_FILE = "token.txt"
COOKIE_NAME = "CPL-coros-token"
LOGIN_URL = "https://t.coros.com/login"
COMMIT_MSG = "chore: update COROS token [skip ci]"


def get_token():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto(LOGIN_URL)

        print("请在浏览器中完成 COROS 登录...")

        token = None
        for _ in range(60):  # 最多 2 分钟
            time.sleep(2)
            for c in context.cookies():
                if c["name"] == COOKIE_NAME:
                    token = c["value"]
                    break
            if token:
                break

        browser.close()
        return token


def save_token(token: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        f.write(f"{token}\n# updated: {ts}\n")
    print("Token 已写入 token.txt")


def git_push():
    subprocess.run(["git", "add", "token.txt"], check=True)
    subprocess.run(["git", "commit", "-m", COMMIT_MSG], check=True)
    subprocess.run(["git", "push"], check=True)
    print("Token 已推送到 GitHub")


def main():
    token = get_token()
    if not token:
        print("❌ 未获取到 token")
        return

    print(f"获取到 token: {token[:20]}...")
    save_token(token)
    git_push()


if __name__ == "__main__":
    main()