#!/usr/bin/env python3
import time
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

# ===== 路径配置（仓库内）=====
TOKEN_FILE = Path(__file__).parent / "token.txt"
COMMIT_MSG = "chore: update COROS token"

# ===== 获取 token =====
def get_token():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://t.coros.com/login")
        print("🏃 请在浏览器中完成 COROS 登录（2 分钟内）")

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

# ===== 写入 token（只一行）=====
def save_token(token: str):
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(f"CPL-coros-token={token}", encoding="utf-8")

# ===== git 推送（强制触发 workflow）=====
def git_commit_push():
    subprocess.run(["git", "add", str(TOKEN_FILE)], check=True)

    # 即使内容相同，也允许提交
    subprocess.run(
        ["git", "commit", "--allow-empty", "-m", COMMIT_MSG],
        check=True
    )

    subprocess.run(["git", "push"], check=True)

def main():
    print("\n🏃 COROS Token 获取工具\n")

    token = get_token()
    if not token:
        raise RuntimeError("❌ 未检测到 token，请确认是否登录成功")

    print(f"✅ 获取 token 成功：{token[:18]}...{token[-6:]}")
    save_token(token)

    print("📤 正在推送到 GitHub...")
    git_commit_push()

    print("\n🎉 完成：GitHub Actions 将自动同步并抓取数据")

if __name__ == "__main__":
    main()