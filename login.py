import asyncio
import pyppeteer
import time
import random
from cred import USERNAME, PASSWORD


class Login:

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

    async def _init(self, options=options_dict):
        """
        init the pyppeteer instance
        """
        self.browser = await pyppeteer.launch(**options)
        self.page = await self.browser.newPage()

    async def main(self, username=USERNAME, password=PASSWORD):
        # browser = await pyppeteer.launch(headless = False)
        # page = await browser.newPage()
        # await page.goto("https://login.taobao.com")
        # input("what ever")
        # await browser.close()
        """
        :param username
        :param password
        """
        await self._init()
        # await self._injection_js()
        await self.page.goto("https://login.taobao.com")
        await self.page.click("form.login-form")
        time.sleep(random.random()*2)
        print(random.random()*2)
        await self.page.type("#fm-login-id", username, {"delay": random.randint(100, 150)})
        await self.page.type("#fm-login-password", password, {"delay": random.randint(100, 150)})
        time.sleep(random.random()*2)

        await self.page.click(".fm-submit")
        # await asyncio.sleep(10000)
        await self.page.waitFor(20)

        try:
            await self.page.waitForNavigation()
        except:
            pass
        try:
            global error
            print("error", error)
            error = await self.page.querySelectorEval(".error", 'node => node.textContent')
        except:
            error = None
        finally:
            if error:
                print("username or password wrong")
            else:
                await asyncio.sleep(800)

        # await self.browser.close()


if __name__ == "__main__":
    login = Login()
    # loop = asyncio.get_event_loop()
    # task = asyncio.ensure_future(login.main())
    # loop.run_until_complete(task)
    asyncio.run(login.main())
