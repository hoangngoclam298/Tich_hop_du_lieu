import scrapy


class IbatdongsanSpider(scrapy.Spider):
    name = "ibatdongsan"
    allowed_domains = ["i-batdongsan.com"]
    start_urls = ["https://i-batdongsan.com"]

    def parse(self, response):
        pass
