import asyncio
import random
import json
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # show browser
        page = await browser.new_page()

        # --- Step 1: Intercept and log payloads ---
        async def log_request(request):
            if request.method == "POST" and "trigger" in request.url:
                try:
                    payload = request.post_data
                    print("\n🔴 Full Payload Captured:\n", json.dumps(json.loads(payload), indent=2))
                except Exception as e:
                    print("⚠️ Error reading payload:", e)

        page.on("request", log_request)

        # --- Step 2: Go to your site ---
        await page.goto("https://workik.com/ai-code-writer", timeout=60000)
        await page.wait_for_timeout(5000)

        # --- Step 3: Open dropdown and select GPT 5 Mini (once) ---
        await page.click("div:has-text('GPT 4.1 Mini')")
        await page.click("text=GPT 5 Mini")
        await page.wait_for_timeout(1500)

        # --- Step 4: Loop sending random messages ---
        messages = ["Hi", "Hello GPT 5 Mini!", "Give me sample code", "Random test", "Ping!", "How are you?"]

        for i in range(5):  # send 5 requests, change number if needed
            msg = random.choice(messages)

            await page.fill("textarea", msg)
            await page.press("textarea", "Enter")

            print(f"\n✅ Sent message {i+1}: {msg}")

            # wait for backend request + reply
            await page.wait_for_timeout(6000)

        await browser.close()

asyncio.run(run())
