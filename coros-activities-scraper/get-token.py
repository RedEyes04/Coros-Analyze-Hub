#!/usr/bin/env python3
"""
COROS Token & Cookies 获取工具（本地运行）

1. 弹出浏览器让用户登录
2. 保存完整 cookies 到 cookies.json
3. 自动 git push 触发 GitHub Actions
"""
import json
import time
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).parent
COOKIES_FILE = BASE_DIR / "cookies.json"
COMMIT_MSG = "chore: update COROS cookies"


def get_cookies_from_browser():
    """通过浏览器登录获取完整 cookies"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # 1️⃣ 打开登录页
        page.goto("https://t.coros.com/login")
        print("👉 请在浏览器中完成 COROS 登录（2 分钟内）")

        # 等待登录成功（检测 token cookie）
        token = None
        for _ in range(60):
            time.sleep(2)
            for c in context.cookies():
                if c["name"] == "CPL-coros-token":
                    token = c["value"]
                    break
            if token:
                print("\n✅ 检测到登录成功！")
                break

        if not token:
            browser.close()
            return None

        # 2️⃣ 关键：访问 activity 页面，补全权限
        print("📥 正在激活 API 权限...")
        page.goto("https://t.coros.com/activity")
        time.sleep(3)

        # 3️⃣ 获取所有 cookies
        all_cookies = context.cookies()
        
        browser.close()
        return all_cookies


def save_cookies(cookies: list):
    """保存 cookies 到文件"""
    COOKIES_FILE.write_text(
        json.dumps(cookies, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"✅ Cookies 已保存到 {COOKIES_FILE}")
    print(f"   共 {len(cookies)} 个 cookie")


def git_commit_push():
    """Git commit 并 push"""
    try:
        # 检查是否有变更
        result = subprocess.run(
            ["git", "status", "--porcelain", str(COOKIES_FILE)],
            capture_output=True, text=True
        )
        
        if not result.stdout.strip():
            print("ℹ️  Cookies 文件无变化，跳过 git push")
            return True
        
        subprocess.run(["git", "add", str(COOKIES_FILE)], check=True)
        subprocess.run(["git", "commit", "-m", COMMIT_MSG], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ Git push 完成")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git 操作失败: {e}")
        return False


def main():
    print("🏃 COROS Cookies 获取工具\n")

    cookies = get_cookies_from_browser()
    
    if not cookies:
        print("❌ 未获取到 cookies，请确认是否登录成功")
        return

    # 找出 token 用于显示
    token = next((c["value"] for c in cookies if c["name"] == "CPL-coros-token"), None)
    if token:
        print(f"🔑 Token: {token[:15]}...{token[-8:]}")

    save_cookies(cookies)

    print("\n📤 推送到 GitHub（触发 Actions）...")
    if git_commit_push():
        print("\n" + "=" * 50)
        print("🎉 完成！GitHub Actions 将自动同步并抓取数据")
        print("=" * 50)


if __name__ == "__main__":
    main()
