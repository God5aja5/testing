import asyncio
import json
import random
import requests
from playwright.async_api import async_playwright

# Telegram bot credentials
BOT_TOKEN = "7803713198:AAHNtjhBl4ecYyF3bwQZg3KG7JPv4dRiPoY"
CHAT_ID = "7265489223"

async def main():
    async with async_playwright() as p:
        print("[*] Launching headless browser...")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        captured_payloads = []

        async def capture_request(route, request):
            try:
                if request.method == "POST":
                    data = request.post_data
                    if data:
                        print(f"[+] Captured request payload: {data[:200]}...")
                        captured_payloads.append(data)
            except Exception as e:
                print(f"[!] Error capturing payload: {e}")
            await route.continue_()

        await page.route("**/*", capture_request)

        print("[*] Navigating to website...")
        await page.goto("https://workik.com/ai-code-write", timeout=60000)

        # --- Select GPT-5 mini ---
        print("[*] Waiting for model dropdown...")
        await page.wait_for_selector("div[role='button']", timeout=20000)

        print("[*] Opening model dropdown...")
        await page.click("div[role='button']")

        print("[*] Selecting GPT-5 mini...")
        await page.click("text=GPT-5 mini")

        # --- Send a random message ---
        random_msg = f"Test message {random.randint(1000,9999)}"
        print(f"[*] Sending message: {random_msg}")
        await page.fill("textarea[placeholder='Ask anything...']", random_msg)
        await page.keyboard.press("Enter")

        print("[*] Waiting for network requests...")
        await page.wait_for_timeout(8000)

        if captured_payloads:
            all_payloads = "\n\n".join(captured_payloads)
            print("\n=== Final Captured Payloads ===\n")
            print(all_payloads)

            msg = f"📡 Captured {len(captured_payloads)} payload(s):\n\n{all_payloads}"
            telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            res = requests.post(telegram_url, data={"chat_id": CHAT_ID, "text": msg[:4000]})
            if res.status_code == 200:
                print("[+] Payloads sent to Telegram successfully.")
            else:
                print(f"[!] Failed to send to Telegram: {res.text}")
        else:
            print("[!] No payloads captured.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
