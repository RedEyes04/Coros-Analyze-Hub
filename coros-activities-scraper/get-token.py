#!/usr/bin/env python3
import time
import subprocess
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

# ===== 路径：永远指向本脚本所在目录 =====
BASE_DIR = Path(__file__).resolve().parent
TOKEN_FILE = BASE_DIR / "token.txt"

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

    TOKEN_FILE.write_text(content, encoding="utf-8")
    print(f"✅ token 已写入：{TOKEN_FILE}")


def git_commit_push():
    diff = subprocess.run(
        ["git", "status", "--porcelain", str(TOKEN_FILE)],
        capture_output=True,
        text=True
    ).stdout.strip()

    if not diff:
        print("⚠️ Git 认为 token 文件无变化（仅用于提示）")

    subprocess.run(["git", "add", str(TOKEN_FILE)], check=True)
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