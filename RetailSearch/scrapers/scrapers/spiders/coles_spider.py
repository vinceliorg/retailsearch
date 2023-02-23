from pathlib import Path

import scrapy


class ColesSpider(scrapy.Spider):
    name = "coles"
    def start_requests(self):
        urls = [
            'https://shop.coles.com.au/a/national/product/coles-elevate-dry-dg-fd-healthy-weight-chicken'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        yield {
            'brand': response.xpath("//span[@class='product-brand']/text()").get()
        }