import scrapy
from ..items import ItemAlonhadat
import time
# -*- coding: utf-8 -*-

class AlonhadatSpider(scrapy.Spider):
    name = "alonhadat"
    allowed_domains = ["alonhadat.com.vn"]
    base_url = "https://alonhadat.com.vn/nha-dat/can-ban/can-ho-chung-cu/trang--"

    def start_requests(self):
        start_urls = [
            "https://alonhadat.com.vn/nha-dat/can-ban/can-ho-chung-cu.html"
        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
        for x in range(1, 1):
            url_page = self.base_url + str(x) + '.html'
            yield scrapy.Request(url=url_page, callback=self.parse)

    def parse(self, response):
        while(response.request.url[25:44] == 'xac-thuc-nguoi-dung'):
            time.sleep(20)
            yield scrapy.Request(url=response.request.url, callback=self.parse)
        products = response.css('.content-item')
        for product in products:
            link_product = product.xpath('div[3]/a/@href').extract_first()
            yield response.follow(link_product, self.parse_product)

    def parse_product(self, response):
        while(response.request.url[25:44] == 'xac-thuc-nguoi-dung'):
            time.sleep(20)
            yield scrapy.Request(url=response.request.url, callback=self.parse_product)
        item = ItemAlonhadat()
        item['title'] = response.css('.property > .title > h1::text').extract_first()
        item['date'] = response.css('.property > .title > span::text').extract_first()
        item['price'] = response.css('.property > .moreinfor > .price > .value::text').extract_first()
        item['area'] = response.css('.property > .moreinfor > .square > .value::text').extract_first()
        item['width'] = response.css('.property > .moreinfor1 > .infor > table > tr:nth-child(4) > td:nth-child(2)::text ').extract_first()
        item['length'] = response.css('.property > .moreinfor1 > .infor > table > tr:nth-child(5) > td:nth-child(2)::text').extract_first()
        item['code'] = response.css('.property > .moreinfor1 > .infor > table > tr:nth-child(1) > td:nth-child(2)::text').extract_first()
        item['direct'] = response.css('.property > .moreinfor1 > .infor > table > tr:nth-child(1) > td:nth-child(4)::text').extract_first()
        item['project'] = response.css('.property > .moreinfor1 > .infor > table  > tr:nth-child(6) > td:nth-child(2) > .project > a::text').extract_first()
        item['description'] = response.css('.property > .detail::text').extract_first()
        item['road_width'] = response.css('.property > .moreinfor1 > .infor > table > tr:nth-child(2) > td:nth-child(4)::text').extract_first()
        item['floor'] = response.css('.property > .moreinfor1 > .infor > table > tr:nth-child(4) > td:nth-child(4)::text').extract_first()
        item['bedroom'] = response.css('.property > .moreinfor1 > .infor > table > tr:nth-child(5) > td:nth-child(4)::text').extract_first()
        item['kitchen'] = response.css('.property > .moreinfor1 > .infor > table > tr:nth-child(2) > td:nth-child(6) > img::attr(src)').extract_first()
        item['diningroom'] = response.css('.property > .moreinfor1 > .infor > table > tr:nth-child(1) > td:nth-child(6) > img::attr(src)').extract_first()
        item['terrace'] = response.css('.property > .moreinfor1 > .infor > table > tr:nth-child(3) > td:nth-child(6) > img::attr(src)').extract_first()
        item['parking'] = response.css('.property > .moreinfor1 > .infor > table > tr:nth-child(4) > td:nth-child(6) > img::attr(src)').extract_first()
        item['address'] = response.css('.property > .address > .value::text').extract_first()
        item['juridical'] = response.css('.property > .moreinfor1 > .infor > table > tr:nth-child(3) > td:nth-child(4)::text').extract_first()
        item['type'] = response.css('.property > .moreinfor1 > .infor > table > tr:nth-child(3) > td:nth-child(2)::text').extract_first()
        item['name_contact'] = response.css('.contact > .contact-info > .content > .name::text').extract_first()
        item['phone_contact'] = response.css('.contact > .contact-info > .content > .fone > a::text').extract_first()
        item['introduce_contact'] = response.css('.contact > .contact-info > .content > .introduce::text').extract_first()
        item['url_page'] = response.request.url
        item['link_image'] = response.css('div.images img::attr(src)').getall()

        yield item
