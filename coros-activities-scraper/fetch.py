import requests
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
TOKEN_FILE = BASE_DIR / "token.txt"
OUT_FILE = BASE_DIR / "activities.json"

# ===== 1. 读取 token / cookie =====
def load_token():
    if not TOKEN_FILE.exists():
        raise RuntimeError("❌ token.txt 不存在")

    token = TOKEN_FILE.read_text().strip()
    if not token:
        raise RuntimeError("❌ token.txt 为空")

    return token


# ===== 2. 构造浏览器级 headers =====
def build_headers(token: str):
    return {
        # ⚠️ 关键：完全模拟浏览器
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/121.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://training.coros.com/",
        "Origin": "https://training.coros.com",

        # ⚠️【核心】Cookie 方式（不是 Bearer）
        "Cookie": token,

        # 某些接口需要
        "X-Requested-With": "XMLHttpRequest",
    }


# ===== 3. token 有效性探测 =====
def check_token(headers):
    test_url = "https://training.coros.com/api/user/profile"

    r = requests.get(test_url, headers=headers, timeout=15)

    if r.status_code == 200:
        print("✅ token 校验成功")
        return

    if r.status_code == 401:
        raise RuntimeError("❌ 401：token 已过期（需要重新抓）")

    if r.status_code == 403:
        raise RuntimeError(
            "❌ 403：token 权限不足\n"
            "👉 请确认你复制的是【完整 Cookie】，不是 accessToken"
        )

    if r.status_code == 404:
        raise RuntimeError(
            "❌ 404：token 校验接口失效\n"
            "👉 COROS 接口路径可能更新，需要重新抓包确认"
        )

    raise RuntimeError(f"❌ token 校验失败：HTTP {r.status_code}")


# ===== 4. 抓取活动数据 =====
def fetch_activities(headers):
    url = (
        "https://training.coros.com/api/activities"
        "?page=1&pageSize=20"
    )

    r = requests.get(url, headers=headers, timeout=20)

    if r.status_code == 200:
        return r.json()

    if r.status_code == 401:
        raise RuntimeError("❌ 401：token 失效")

    if r.status_code == 403:
        raise RuntimeError(
            "❌ 403：接口被拒绝\n"
            "👉 99% 是 Cookie 不完整 / UA 不一致"
        )

    if r.status_code == 404:
        raise RuntimeError(
            "❌ 404：activities 接口不存在\n"
            "👉 请重新抓包确认真实路径"
        )

    raise RuntimeError(f"❌ 抓取失败：HTTP {r.status_code}")


# ===== 5. 主流程 =====
def main():
    print("📡 开始抓取 COROS 活动数据")

    token = load_token()
    headers = build_headers(token)

    check_token(headers)

    data = fetch_activities(headers)

    OUT_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2)
    )

    print(f"✅ 抓取成功，已保存到 {OUT_FILE}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(str(e))
        sys.exit(1)