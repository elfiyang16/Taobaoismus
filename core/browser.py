import asyncio
import pyppeteer


class PageSession:

    pyppeteer.DEBUG = True
    # page = None
    options_dict = {
        "headless": False,
        "args": [
            '--window-size={1300},{600}'
            '--disable-extensions',
            '--hide-scrollbars',
            '--disable-bundled-ppapi-flash',
            '--mute-audio',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-gpu',
            '--disable-infobars'
        ],
        "dumpio": True,
        "autoClose": False
    }

    # async def _injection_js(self):
    # """
    # change webdriver value to bypass anti-crawler detection
    # """
    # await self.page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
    #                                   '{ webdriver:{ get: () => false } }) }')

    # def __init__(self, url):
    #     self.url = url

    # async def _init(self, options=options_dict):
    #     self.browser = await pyppeteer.launch(**options)
    #     self.page = await self.browser.newPage()

    async def __aenter__(self, options=options_dict):
        self.browser = await pyppeteer.launch(**options)
        self.page = await self.browser.newPage()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.browser.close()
