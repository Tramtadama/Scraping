import scrapy
from scrapy.crawler import CrawlerProcess


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = ['https://www.hornbach.cz/mvc/hbprice/article-tracking-prices/6097676/0']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

process = CrawlerProcess()
process.crawl(QuotesSpider)
process.start()
