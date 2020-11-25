import asyncio
import pyppeteer
import time
import random
from cred import USERNAME, PASSWORD
from vendor_list import vendor_dict
from core import browser
import requests

TAOBAO_URL = "https://login.taobao.com"


class Taobao:
    def __init__(self, url, session):
        self.url = url
        self.session = session
        self.page = session.page

    # async def _injection_js(self, page):
    #     """注入js
    #     """
    #     await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
    #                                      '{ webdriver:{ get: () => false } }) }')
    async def evaluate(self, func, *params):
        res = await self.page.evaluate(func, *params)
        return res

    async def get_elem(self, selector: str) -> str:
        return await self.page.querySelector(selector)

    async def login(self, username=USERNAME, password=PASSWORD):
        """
        :param username
        :param password
        """
        # await self._injection_js(page)
        await self.page.goto(self.url, timeout=10000000)

        await self.page.click("form.login-form")
        time.sleep(random.random()*2)

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

    async def check_price(self, product_url):
        """
        :param product_url --> string
        """

    async def check_products(self, product_name, product_cat):
        """
        :param product_name --> string
        :param product_cat --> string, match vendor_list key
        """
        ele = await self.get_elem('#browsercontext-class > dl > dd')
        p = await ele.querySelectorAllEval('p', 'nodes => nodes.map(n=>n.innerHTML)')


if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    # task = asyncio.ensure_future(login.main())
    # loop.run_until_complete(task)

    async def main():
        async with browser.PageSession() as page_session:
            taobao = Taobao(TAOBAO_URL, page_session)
            await taobao.login()
            # final_html = await page_session.page.content()

    asyncio.run(main())
