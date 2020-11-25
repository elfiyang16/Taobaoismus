## Taobao Scraping

The goal is to scrape lists of product info from Taobao and dump it into Google Sheet

_Note_

Taobao implements strong anti-scraping mechanism against common web crawlers using Selenium etc. Even I use pyppeteer here, there's still some extra steps in order to bypass the check:

```python
# launcher.py in Pyppeteer

DEFAULT_ARGS = [
    # '--enable-automation', COMMENT THIS LINE OUT
    '--password-store=basic',
    '--use-mock-keychain',
]

```

Before you implement the above code, `window.navigator.webdriver` will evaluate to `True` in the automated browser, which leads to Taobao detecting the crawler and blocking the bot. But this will evaluate to `undefined` afterwards :).

MVP:

- create something that can run through list of product names and cats provided using a list of shops
- check each product's stock, price
- update the spreadsheet on product stock, price
- (update product url if not exist?)
- alert the owner
- implement logging
