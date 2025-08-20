import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # Launch browser in headless mode
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Intercept network requests
        async def capture_request(route, request):
            if "chat" in request.url and request.method == "POST":
                print("---- Captured Payload ----")
                print("URL:", request.url)
                print("Headers:", request.headers)
                print("Post Data:", request.post_data())
                print("-------------------------")
            await route.continue_()

        await context.route("**/*", capture_request)

        # Go to the website
        await page.goto("https://chatgpt.ch/")  # replace with real site

        # Select GPT-5 mini (instead of default GPT-4)
        await page.click("text=GPT-4")  # open dropdown
        await page.click("text=GPT-5 mini")  # select GPT-5 mini

        # Type a message
        await page.fill("textarea", "Hello from headless script!")
        await page.press("textarea", "Enter")

        # Wait for some response
        await page.wait_for_timeout(5000)

        await browser.close()

asyncio.run(main())
