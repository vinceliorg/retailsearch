# woolworth links
from pathlib import Path

import scrapy
from scrapy_playwright.page import PageMethod



class WSLSpider(scrapy.Spider):
    name = "wsl"
    custom_settings = {
        "PLAYWRIGHT_CONTEXTS": {
            "default": {
            "proxy": {
                "server": "http://sydney.wonderproxy.com:11000",
                "username": "vli",
                "password": "@881106Vl"
                }},
            "alternative": {
            "proxy": {
                "server": "http://melbourne.wonderproxy.com:11000",
                "username": "vli",
                "password": "@881106Vl"
                },
    },
        }
    }

    def start_requests(self):        
        filename = '/Users/vli/Work/RetailSearch/RetailSearch/scrapers/coles_scraper/wws_prod_urls_1.csv'
        with open(filename) as file:
            urls = [line.rstrip() for line in file]
        # urls = ['https://www.woolworths.com.au/shop/productdetails/763597/selleys-oven-cleaner-wipes']
        for url in urls:
            yield scrapy.Request(url, meta=dict(
                playwright = True,
                playwright_include_page = True, 
                playwright_page_methods =[PageMethod('wait_for_selector', 'span.price-cents')],
                errback=self.errback,
            ))

    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.close()

        yield {
            'title': response.xpath('//h1/text()').get(),
            'price': response.xpath('//span[@class="price-dollars"]/text()').get(),
            'price-centsPer': response.xpath('//span[@class="price-cents"]/text()').get(),
            'package-price': response.xpath('//div[@class="shelfProductTile-cupPrice"]/text()').get(),
            'product-details': response.xpath('//h2[@class="product-heading"]/following-sibling::div/text()').get(),
            'ingredents': response.xpath('//section[@class="ingredients"]').get(),
            'allergy': response.xpath('//section[@class="allergen"]').get()
        }
    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()