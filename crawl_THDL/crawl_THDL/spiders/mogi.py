import scrapy
from ..items import ItemMogi
import time
# -*- coding: utf-8 -*-

class NhatotSpider(scrapy.Spider):
    name = "mogi"
    allowed_domains = ["mogi.vn"]
    base_url = "https://mogi.vn/mua-can-ho-chung-cu?cp="

    def start_requests(self):
        start_urls = [
            "https://mogi.vn/mua-can-ho-chung-cu"
        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
        for x in range(1, 3193):
            url_page = self.base_url + str(x)
            yield scrapy.Request(url=url_page, callback=self.parse)

    def parse(self, response):
        products = response.css('#property > div.property-listing > ul > li')
        for product in products:
            link_product = product.css('.prop-info a::attr(href)').extract_first()
            print(link_product)
            yield scrapy.Request(link_product, self.parse_product)

    def parse_product(self, response):
        item = ItemMogi()
        item['title'] = response.css('#mogi-page-content > div.property-detail.clearfix > div.property-detail-main > div.main-info > div.title > h1::text').extract_first()
        item['price'] = response.xpath('//*[@id="mogi-page-content"]/div[2]/div[1]/div[2]/div[3]/text()').extract_first()
        item['address'] = response.css('#mogi-page-content > div.property-detail.clearfix > div.property-detail-main > div.main-info > div.address::text').extract_first()
        item['area'] = response.xpath('//*[@id="mogi-page-content"]/div[2]/div[1]/div[2]/div[5]/div[1]/span[2]/text()').extract_first()
        item['date'] = response.css('#mogi-page-content > div.property-detail.clearfix > div.property-detail-main > div.main-info > div.info-attrs.clearfix > div:nth-child(5) > span:nth-child(2)::text').extract_first()
        item['description'] = response.xpath('//*[@id="mogi-page-content"]/div[2]/div[1]/div[2]/div[6]/text()').getall()
        item['code'] = response.css('#mogi-page-content > div.property-detail.clearfix > div.property-detail-main > div.main-info > div.info-attrs.clearfix > div:nth-child(6) > span:nth-child(2)::text').extract_first()
        item['juridical'] = response.css('#mogi-page-content > div.property-detail.clearfix > div.property-detail-main > div.main-info > div.info-attrs.clearfix > div:nth-child(4) > span:nth-child(2)::text').extract_first()
        item['bathroom'] = response.css('#mogi-page-content > div.property-detail.clearfix > div.property-detail-main > div.main-info > div.info-attrs.clearfix > div:nth-child(3) > span:nth-child(2)::text').extract_first()
        item['bedroom'] = response.css('#mogi-page-content > div.property-detail.clearfix > div.property-detail-main > div.main-info > div.info-attrs.clearfix > div:nth-child(2) > span:nth-child(2)::text').extract_first()
        item['url_page'] = response.request.url
        item['link_image'] = response.css('#top-media img::attr(data-src)').getall()
        item['link_image'].append(response.css('#top-media img::attr(src)').extract_first())
        url_contact = response.css('#mogi-page-content > div.property-detail.clearfix > div.property-detail-main > div.main-info > div.agent-info > div.agent-name > a::attr(href)').extract_first()
        try:
            url_contact = 'https://mogi.vn' + url_contact
            print(url_contact)
            yield scrapy.Request(url_contact, self.parse_contact, meta={'item': item})
        except:
            item['name_contact'] = ''
            item['phone_contact'] = ''
        yield item

    def parse_contact(self, response):
        name = response.css('#agent > div.info > h1::text').extract_first()
        phone = response.css('#agent > div.info > div.agent-phone > a::text').extract_first()
        item = response.meta.get('item', {})
        item['name_contact'] = name
        item['phone_contact'] = phone
        yield item