import json
import time
from playwright.sync_api import sync_playwright

EMAIL = "1572166648@qq.com"
PASSWORD = "zhou622.."
OUTPUT_FILE = "../public/activities_data.json"

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )
    page = browser.new_page()

    # 打开登录页
    page.goto("https://t.coros.com/login", wait_until="networkidle")
    page.wait_for_timeout(3000)

    # 截图（CI 排错用）
    page.screenshot(path="debug-login.png", full_page=True)

    # ===== 输入账号 =====
    email_input = page.get_by_role("textbox").first
    email_input.wait_for(state="visible", timeout=30000)
    email_input.fill(EMAIL)

    # ===== 输入密码 =====
    password_input = page.locator("input[type='password']")
    password_input.wait_for(state="visible", timeout=30000)
    password_input.fill(PASSWORD)

    # ===== 勾选隐私政策（点 label 本身最稳）=====
    page.locator("label.arco-checkbox").first.click()
    page.wait_for_timeout(500)

    # ===== 提交登录 =====
    page.locator("button[type='submit']").click()
    page.wait_for_load_state("networkidle")
    time.sleep(3)

    # ===== 进入 Activities 页面 =====
    page.goto("https://t.coros.com/admin/views/activities", wait_until="networkidle")
    time.sleep(3)

    # 等待表格首条数据出现
    page.wait_for_selector("tr.arco-table-tr", timeout=30000)

    # ===== 抓取训练数据 =====
    activities = page.evaluate("""
    () => {
        const rows = Array.from(document.querySelectorAll('tr.arco-table-tr'));
        return rows.map(row => {
            const name = row.querySelector('.activity-name a.detail-link')?.textContent?.trim();
            if (!name) return null;

            return {
                day: row.querySelector('.day-str')?.textContent?.trim() || '',
                name,
                distance: row.querySelector('td:nth-child(6) span')?.textContent?.trim() || '',
                duration: row.querySelector('td:nth-child(7) span')?.textContent?.trim() || '',
                pace: row.querySelector('td:nth-child(8) span')?.textContent?.trim() || '',
                avg_hr: row.querySelector('td:nth-child(9) span')?.textContent?.trim() || '',
                training_load: row.querySelector('td:nth-child(10) span')?.textContent?.trim() || ''
            };
        }).filter(Boolean);
    }
    """)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(activities, f, ensure_ascii=False, indent=4)

    print(f"抓取完成，共抓到 {len(activities)} 条训练数据")

    browser.close()