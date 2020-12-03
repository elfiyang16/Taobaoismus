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
    async def mouse_slider(self):
        """
        :return: None if fail Or True if succeed
        """
        await asyncio.sleep(3)
        try:
            await self.page.hover('#nc_1_n1z')
            await self.page.mouse.down()
            await self.page.mouse.move(1000, 0, {'steps': 30})
            await self.page.mouse.up()
            print("slider shows")

            await asyncio.sleep(2)
        except Exception as e:
            print(e, '     :slider login error')
            return None
        else:
            await asyncio.sleep(3)
            ua = await self.page.evaluate('navigator.webdriver')
            print(ua)
            await self.page.screenshot({'path': './headless-slide-result.png'})
            slider_again = await self.page.querySelectorEval('#nc_1__scale_text', 'node => node.textContent')
            if slider_again != '验证通过':
                return None
            else:
                await self.page.screenshot({'path': './headless-slide-result.png'})
                print('Authentication pass')
                return True

    async def evaluate(self, func, *params):
        res = await self.page.evaluate(func, *params)
        return res

    async def get_elem(self, selector: str) -> str:
        return await self.page.querySelector(selector)

    async def get_elems(self, selector: str) -> list:
        return await self.page.querySelectorAll(selector)

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
            # else:
            #     await asyncio.sleep(800)

    # async def find_vendor(self,  vendor_key: str, vendor_dict=vendor_dict):
    #     vendor_list = vendor_dict[vendor_key]
    #     for vendor in vendor_list:
    #         # Grab a list of products for this vendor category
    #         # that date not match or starred
    #         product_lists =

    async def check_price(self, product_url):
        """
        :param product_url --> string
        : qualified_sale: 30
        """
        QUALIFIED_SALE = 30

        await self.page.goto(product_url, timeout=10000000)
        await asyncio.sleep(3)

        # CHECK SLIDER
        slider = None
        try:
            slider = await self.page.querySelectorEval('#nocaptcha', 'node => node.style')
            print(slider)

            if slider:
                print('Authentication required')
                flag = await self.mouse_slider()
                if not flag:
                    print('Authentication failed')
                    return None
                time.sleep(random.random() + 0.5)
                print("evalutae 3")
                await asyncio.sleep(10)
            else:
                print('No authentication required')
                pass
        except:
            pass

        prod_title = await self.get_elem('div.tb-detail-hd > h1')
        prod_title_text = await self.page.evaluate('''(element) => element.textContent''', prod_title)
        print(prod_title_text)

        prod_sale_count = await self.get_elem("#J_DetailMeta > div.tm-clear > div.tb-property > div > ul > li.tm-ind-item.tm-ind-sellCount > div > span.tm-count")
        print("prod_sale_count", prod_sale_count)

        prod_sale_count_text = await self.page.evaluate('''(element) => element.textContent''', prod_sale_count)
        print("prod_sale_count_text", prod_sale_count_text)
        if int(prod_sale_count_text) < QUALIFIED_SALE:
            raise Exception(f"{prod_sale_count_text} is below qualified sale")

        # prod_categories = await self.get_elems('div.tb-sku > dl.tb-prop.tm-sale-prop.tm-clear > dt.tb-metatit')
        prod_categories = await self.get_elems("#J_DetailMeta > div.tm-clear > div.tb-property > div > div.tb-key > div > div > dl.tb-prop.tm-sale-prop.tm-clear > dd > ul")
        print("prod_categories", prod_categories)
        # [<pyppeteer.element_handle.ElementHandle object at 0x10d7c5e10>, <pyppeteer.element_handle.ElementHandle object at 0x10d7c2250>]
        prod_categories_texts = []
        for cate in prod_categories:
            attr = await self.page.evaluate('''el => el.getAttribute("data-property")''', cate)
            print(attr) #  颜色分类 套餐类型

          #  attr = await self.page.querySelectorEval("span.styleNumber", 'el => el.map(x => x.getAttribute("data-property"))');

            cate_name1 = await cate.getProperty('data-property')
            print("cate_name1", cate_name1)
            cate_name2 = await (await cate.getProperty('data-property')).jsonValue()
            print("cate_name2", cate_name2)
            prod_categories_texts.append(attr)

        # prod_categories_text = [self.evaluate(
        #     '''(element) => element.data-property''', cate) for cate in prod_categories]
        # prod_categories_text = [cate.getProperty(
        #     'data-property') for cate in prod_categories]
        # print(prod_categories_text)

        # cate_results = await asyncio.gather(*cate_results2, return_exceptions=True)
        # cate_results = await asyncio.gather(*prod_categories_text, return_exceptions=True)
        print("prod_categories_texts", prod_categories_texts)
        # 【'颜色分类', '套餐类型']
        if len(prod_categories_texts) == 0:
            print("No category info")
        elif '颜色分类' in prod_categories_texts and len(prod_categories_texts) == 1:
            print("Only color category exist")
            
        else:
            print("Multiple categories exist")
            cate_color_prods =  await self.get_elems("#J_DetailMeta > div.tm-clear > div.tb-property > div > div.tb-key > div > div > dl.tb-prop.tm-sale-prop.tm-clear > dd > ul[data-property='颜色分类']> li")
            print("cate_color_prods", cate_color_prods)
            for prod in cate_color_prods:
                #  ==> Get product name
                prod_title = await self.page.evaluate('''el => el.getAttribute("title")''', prod)
                print("prod_title", prod_title)
                #  ==> Click the product
                await self.page.click(f"li[title='{prod_title}'] > a > span")

                time.sleep(random.random()*2)
                await self.page.screenshot({'path': f"product_{prod_title}.png"})
                #  ==> Get the stock
                prod_stock = await self.get_elem("#J_EmStock")
                prod_stock_text = await self.page.evaluate('''(element) => element.textContent''', prod_stock)
                time.sleep(random.random()*2)
                print("prod_stock", prod_stock_text)
                #  ==> Get the price
                prod_price = await self.get_elem("#J_PromoPrice > dd > div > span")
                prod_price_text = await self.page.evaluate('''(element) => element.textContent''', prod_price)
                time.sleep(random.random()*2)
                print("prod_price", prod_price_text)
                #  ==> Defaults to first option in 套餐类型



                 
                
            
        # [(await cate.getProperty('data-property'))for cate in prod_categories]
        # prod_categories_text = await (await item.getProperty('data-property')).jsonValue()

        # for cate in prod_categories:
        #     url = await page.evaluate('link => link.href', link)

        # p = await ele.querySelectorAllEval('p', 'nodes => nodes.map(n=>n.innerHTML)')

    async def check_products(self, product_name, product_cat):
        """
        :param product_name --> string
        :param product_cat --> string, match vendor_list key
        """


if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    # task = asyncio.ensure_future(login.main())
    # loop.run_until_complete(task)

    prod_url = "https://detail.tmall.com/item.htm?id=628686026534&ns=1&abbucket=11&skuId=4460326940308"

    async def main():
        async with browser.PageSession() as page_session:
            taobao = Taobao(TAOBAO_URL, page_session)
            await taobao.login()
            await taobao.check_price(prod_url)
            # final_html = await page_session.page.content()

    asyncio.run(main())
