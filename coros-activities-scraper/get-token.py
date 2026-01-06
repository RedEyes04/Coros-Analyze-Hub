#!/usr/bin/env python3
"""
COROS Token 获取脚本（本地运行）

功能：
1. 弹出浏览器让用户手动登录 COROS
2. 检测登录成功后获取 token
3. 将 token 保存到文件
4. 自动 git commit & push 到仓库

使用方式：
    python get-token.py
"""

import os
import time
import subprocess
from datetime import datetime
from playwright.sync_api import sync_playwright

# 配置
TOKEN_FILE = "token.txt"
GIT_COMMIT_MSG = "chore: update COROS token"


def get_token_from_browser():
    """通过浏览器登录获取 COROS token"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://t.coros.com/login")
        print("=" * 50)
        print("请在弹出的浏览器中登录 COROS...")
        print("登录成功后脚本会自动检测并继续")
        print("=" * 50)

        # 等待 token（最多等 2 分钟）
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

        browser.close()
        return token


def save_token(token: str):
    """保存 token 到文件（带时间戳）"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"{token}\n# Updated: {timestamp}\n"
    
    with open(TOKEN_FILE, "w") as f:
        f.write(content)
    
    print(f"✅ Token 已保存到 {TOKEN_FILE}")


def git_push():
    """Git commit 并 push"""
    try:
        # 检查是否有变更
        result = subprocess.run(
            ["git", "status", "--porcelain", TOKEN_FILE],
            capture_output=True,
            text=True
        )
        
        if not result.stdout.strip():
            print("ℹ️  Token 文件无变化，跳过 git push")
            return True
        
        # Git add
        subprocess.run(["git", "add", TOKEN_FILE], check=True)
        print("✅ git add 完成")
        
        # Git commit
        subprocess.run(
            ["git", "commit", "-m", GIT_COMMIT_MSG],
            check=True
        )
        print("✅ git commit 完成")
        
        # Git push
        subprocess.run(["git", "push"], check=True)
        print("✅ git push 完成")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git 操作失败: {e}")
        return False


def main():
    print("\n🏃 COROS Token 获取工具\n")
    
    # Step 1: 获取 token
    token = get_token_from_browser()
    
    if not token:
        print("❌ 未能获取到 token，请确认是否登录成功")
        return
    
    print(f"📝 Token: {token[:20]}...{token[-10:]}")
    
    # Step 2: 保存 token
    save_token(token)
    
    # Step 3: Git push
    print("\n📤 正在推送到 GitHub...")
    if git_push():
        print("\n" + "=" * 50)
        print("🎉 完成！Token 已推送到 GitHub")
        print("   GitHub Actions 将自动触发服务器抓取")
        print("=" * 50)
    else:
        print("\n⚠️  Git push 失败，请手动推送")


if __name__ == "__main__":
    main()
