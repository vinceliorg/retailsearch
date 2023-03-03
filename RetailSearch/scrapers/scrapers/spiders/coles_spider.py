from pathlib import Path

import scrapy


class ColesSpider(scrapy.Spider):
    name = "coles"
    def start_requests(self):
        filename = '/Users/vli/Work/RetailSearch/RetailSearch/scrapers/coles_scraper/coles_prod_urls_v2_8.csv'
        with open(filename) as file:
            urls = [line.rstrip() for line in file]
        for url in urls:
            yield scrapy.Request(url, meta={"playwright": True})

    def parse(self, response):
        yield {
            'title': response.xpath('//h1[@data-testid="title"]/text()').get(),
            'price': response.xpath('//span[@data-testid="pricing"]/text()').get(),
            'package_price': response.xpath('//span[@class="price__calculation_method"]/text()').get(),
            'product_image': response.xpath('//img[@data-testid="product-image-0"]/@src').get(),
            'product_details': response.xpath('//div[@data-testid="section-header"]').get(),
            'url': response.url
        }