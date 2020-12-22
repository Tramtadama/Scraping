import json
import scrapy


class ProductSpider(scrapy.Spider):
    name = "product"
    
    def start_requests(self):
        with open('merkury_products.json') as f:
            products = json.load(f)

        product_list = []
        for product in products:
             if product['product_link']:
                product_list.append(product['product_link'])

        for product in product_list:
            yield scrapy.Request(url=product, callback=self.parse)

    def parse(self, response):
    
        yield {'name': response.css('div.naglowek h1.tytul::text').getall()[0].strip("\t"),
                'code': response.css('span.value.js-kod::text').get(),
                'price': response.css('div.produkt-prawa p.cena span::text').get(),
                'url': response.request.url
                }
