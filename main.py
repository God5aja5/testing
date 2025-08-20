#772
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # Launch Chromium in headless mode
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Capture POST requests (chat messages)
        async def capture_request(route, request):
            if request.method == "POST" and "chat" in request.url.lower():
                print("---- Captured Payload ----")
                print("URL:", request.url)
                print("Headers:", request.headers)
                print("Post Data:", request.post_data())
                print("-------------------------")
            await route.continue_()  # ✅ must be exactly this

        await context.route("**/*", capture_request)

        # Go to your site
        await page.goto("https://workik.com/ai-code-writer")

        # Open dropdown and select GPT-5 mini
        await page.click("text=GPT-4")       # opens dropdown
        await page.click("text=GPT-5 mini")  # selects GPT-5 mini

        # Type and send a random message
        await page.fill("textarea", "Hello from Playwright headless!")
        await page.press("textarea", "Enter")

        # Wait for network to process
        await page.wait_for_timeout(5000)

        await browser.close()

asyncio.run(main())
