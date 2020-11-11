import asyncio
import pyppeteer

pyppeteer.DEBUG = True

async def main():
  browser = await pyppeteer.launch(headless = False)
  page = await browser.newPage()
  await page.goto("https://login.taobao.com")
  input("what ever")
  await browser.close()
  

if __name__ == "__main__":
  asyncio.get_event_loop().run_until_complete(main())