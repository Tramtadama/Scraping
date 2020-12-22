import scrapy
import json

class BaumaxSpider(scrapy.Spider):
    name = "baumax"
    
    def start_requests(self):
        with open('baumax_urls.json') as f:
            urls = json.load(f)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        
        if not response.css('div.result.with-img a'):
            product_link = []
        else:
            product_link = response.css('div.result.with-img a').attrib['href']

        yield{'product_link': product_link,
                'url': response.request.url}
