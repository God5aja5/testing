import asyncio
import json
import random
import requests
from playwright.async_api import async_playwright

BOT_TOKEN = "7803713198:AAHNtjhBl4ecYyF3bwQZg3KG7JPv4dRiPoY"
CHAT_ID = "7265489223"

async def main():
    async with async_playwright() as p:
        print("[*] Launching headless browser...")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        captured_payloads = []

        async def capture_request(route, request):
            if request.method == "POST":
                data = request.post_data
                if data:
                    print(f"[+] Captured payload: {data[:200]}...")
                    captured_payloads.append(data)
            await route.continue_()

        await page.route("**/*", capture_request)

        print("[*] Navigating to website...")
        await page.goto("https://workik.com/ai-code-write", timeout=60000)

        # --- Open dropdown ---
        print("[*] Clicking GPT-4 dropdown...")
        await page.locator("//span[contains(text(),'GPT-4')]").click()

        # --- Select GPT-5 mini ---
        print("[*] Selecting GPT-5 mini...")
        await page.locator("//span[contains(text(),'GPT-5 mini')]").click()

        # --- Send random message ---
        random_msg = f"Hello {random.randint(1000,9999)}"
        print(f"[*] Sending: {random_msg}")
        await page.fill("textarea", random_msg)
        await page.keyboard.press("Enter")

        print("[*] Waiting for requests...")
        await page.wait_for_timeout(8000)

        if captured_payloads:
            all_payloads = "\n\n".join(captured_payloads)
            print("\n=== Captured Payloads ===\n")
            print(all_payloads)

            msg = f"📡 Got {len(captured_payloads)} payload(s):\n\n{all_payloads}"
            telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            res = requests.post(telegram_url, data={"chat_id": CHAT_ID, "text": msg[:4000]})
            if res.status_code == 200:
                print("[+] Sent to Telegram ✅")
            else:
                print(f"[!] Telegram send failed: {res.text}")
        else:
            print("[!] No payloads captured.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
