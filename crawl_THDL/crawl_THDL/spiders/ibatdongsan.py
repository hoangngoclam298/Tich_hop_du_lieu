import scrapy
from ..items import ItemIbatdongsan
import time
# -*- coding: utf-8 -*-

class IbatdongsanSpider(scrapy.Spider):
    name = "ibatdongsan"
    allowed_domains = ["i-batdongsan.com"]
    base_urls = ["https://i-batdongsan.com"]

    def start_requests(self):
        start_urls = [
            "https://i-batdongsan.com/can-ban-can-ho-chung-cu.htm"
        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        products = response.css('.content-item')
        for product in products:
            link_product = product.css('.text > .ct_title > a::attr(href)').extract_first()
            yield response.follow(link_product, self.parse_product)

    def parse_product(self, response):
        item = ItemIbatdongsan()
        item['title'] = response.css('.property > .title > h1::text').extract_first()
        item['price'] = response.css('.property > .moreinfor1 > .infor > table > tr:nth-child(7) > td:nth-child(4)::text').extract_first()
        item['address'] = response.css('.property > .contact > .address > .value::text ').extract()
        item['area'] = response.css('.property > .moreinfor1 > .infor > table > tr:nth-child(7) > td:nth-child(2)::text').extract_first()
        item['date'] = response.css('.property > .moreinfor1 > .infor > table > tr:nth-child(1) > td:nth-child(2)::text').extract_first()
        item['description'] = response.css('.property > .detail::text').extract_first()
        item['code'] = response.css('.property > .moreinfor1 > .infor > table > tr:nth-child(2) > td:nth-child(2)::text').extract_first()
        item['type'] = response.css('.property > .moreinfor1 > .infor > table > tr:nth-child(4) > td:nth-child(2)::text').extract_first()
        item['width'] = response.css('.property > .moreinfor1 > .infor > table > tr:nth-child(5) > td:nth-child(2)::text').extract_first()
        item['length'] = response.css('.property > .moreinfor1 > .infor > table > tr:nth-child(6) > td:nth-child(2)::text').extract_first()
        item['direct'] = response.css('.property > .moreinfor1 > .infor > table > tr:nth-child(2) > td:nth-child(4)::text').extract_first()
        item['road_width'] = response.css('.property > .moreinfor1 > .infor > table > tr:nth-child(3) > td:nth-child(4)::text').extract_first()
        item['juridical'] = response.css('.property > .moreinfor1 > .infor > table > tr:nth-child(4) > td:nth-child(4)::text').extract_first()
        item['floor'] = response.css('.property > .moreinfor1 > .infor > table > tr:nth-child(5) > td:nth-child(4)::text').extract_first()
        item['bedroom'] = response.css('.property > .moreinfor1 > .infor > table > tr:nth-child(6) > td:nth-child(4)::text').extract_first()
        item['name_contact'] = response.css('.property > .contact > .contact-info > .content > .name::text').extract_first()
        item['phone_contact'] = response.css('.property > .contact > .contact-info > .content > .fone > a::text').extract_first()
        item['kitchen'] = response.css('.property > .moreinfor1 > .infor > table > tr:nth-child(3) > td:nth-child(6) > img::attr(src)').extract_first()
        item['diningroom'] = response.css('.property > .moreinfor1 > .infor > table > tr:nth-child(2) > td:nth-child(6)> img::attr(src)').extract_first()
        item['terrace'] = response.css('.property > .moreinfor1 > .infor > table > tr:nth-child(4) > td:nth-child(6) > img::attr(src)').extract_first()
        item['parking'] = response.css('.property > .moreinfor1 > .infor > table > tr:nth-child(5) > td:nth-child(6) > img::attr(src)').extract_first()
        item['url_page'] = response.request.url
        item['link_image'] = response.css('div.images img::attr(src)').getall()

        yield item