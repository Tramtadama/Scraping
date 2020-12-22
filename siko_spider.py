import scrapy
from scrapy.crawler import CrawlerProcess


class SikoSpider(scrapy.Spider):
    name = "siko"

    def start_requests(self):
        with open('siko_urls.txt') as f:
            urls = f.read().splitlines()
            
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        yield{
            'price': response.xpath('//meta[@itemprop="price"]').attrib['content'],
            'name': response.xpath('//meta[@property="og:title"]').attrib['content'],
            'url': response.request.url
                }
