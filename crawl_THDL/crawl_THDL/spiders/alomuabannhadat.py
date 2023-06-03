import scrapy
from ..items import ItemAlomuabannhadat
import time
# -*- coding: utf-8 -*-

class AlomuabannhadatSpider(scrapy.Spider):
    name = "alomuabannhadat"
    allowed_domains = ["alomuabannhadat.vn"]
    base_url = "https://alomuabannhadat.vn/nha-ban/ban-can-ho-chung-cu/"

    def start_requests(self):
        start_urls = [
            "https://alomuabannhadat.vn/nha-ban/ban-can-ho-chung-cu/"
        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        products = response.css('.wrap-property > .property')
        print(len(products))
        for product in products:
            link_product = product.css('.info > a::attr(href)').extract_first()
            print(link_product)
            yield scrapy.Request(link_product, self.parse_product)
            break

    def parse_product(self, response):
        item = ItemAlomuabannhadat()
        item['title'] = response.css('#property-detail h1::text').extract_first()

        item['price'] = response.xpath(
            '/html/body/div[1]/div[3]/div[2]/div/div[1]/section/div/div[1]/section/dl/dd[2]/span/text()').extract_first()
        """
        item['address'] = response.css('.property > .contact > .address > .value::text ').extract()
        item['area'] = response.css(
            '.property > .moreinfor1 > .infor > table > tr:nth-child(7) > td:nth-child(2)::text').extract_first()
        item['date'] = response.css(
            '.property > .moreinfor1 > .infor > table > tr:nth-child(1) > td:nth-child(2)::text').extract_first()
        item['brief'] = response.css('.property > .detail::text').extract_first()
        item['code'] = response.css(
            '.property > .moreinfor1 > .infor > table > tr:nth-child(2) > td:nth-child(2)::text').extract_first()
        item['type'] = response.css(
            '.property > .moreinfor1 > .infor > table > tr:nth-child(4) > td:nth-child(2)::text').extract_first()
        item['width'] = response.css(
            '.property > .moreinfor1 > .infor > table > tr:nth-child(5) > td:nth-child(2)::text').extract_first()
        item['length'] = response.css(
            '.property > .moreinfor1 > .infor > table > tr:nth-child(6) > td:nth-child(2)::text').extract_first()
        item['direct'] = response.css(
            '.property > .moreinfor1 > .infor > table > tr:nth-child(2) > td:nth-child(4)::text').extract_first()
        item['world_highway'] = response.css(
            '.property > .moreinfor1 > .infor > table > tr:nth-child(3) > td:nth-child(4)::text').extract_first()
        item['juridical'] = response.css(
            '.property > .moreinfor1 > .infor > table > tr:nth-child(4) > td:nth-child(4)::text').extract_first()
        item['floor'] = response.css(
            '.property > .moreinfor1 > .infor > table > tr:nth-child(5) > td:nth-child(4)::text').extract_first()
        item['bedroom'] = response.css(
            '.property > .moreinfor1 > .infor > table > tr:nth-child(6) > td:nth-child(4)::text').extract_first()
        item['name_contact'] = response.css(
            '.property > .contact > .contact-info > .content > .name::text').extract_first()
        item['phone_contact'] = response.css(
            '.property > .contact > .contact-info > .content > .fone > a::text').extract_first()
        item['kitchen'] = response.css(
            '.property > .moreinfor1 > .infor > table > tr:nth-child(3) > td:nth-child(6) > img::attr(src)').extract_first()
        item['diningroom'] = response.css(
            '.property > .moreinfor1 > .infor > table > tr:nth-child(2) > td:nth-child(6)> img::attr(src)').extract_first()
        item['terrace'] = response.css(
            '.property > .moreinfor1 > .infor > table > tr:nth-child(4) > td:nth-child(6) > img::attr(src)').extract_first()
        item['parking'] = response.css(
            '.property > .moreinfor1 > .infor > table > tr:nth-child(5) > td:nth-child(6) > img::attr(src)').extract_first()
        item['url_page'] = response.request.url
        item['link_image'] = response.css('div.images img::attr(src)').getall()
        """

        yield item
