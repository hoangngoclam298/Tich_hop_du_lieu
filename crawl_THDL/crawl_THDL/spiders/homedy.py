import scrapy
from ..items import ItemHomedy
import time
# -*- coding: utf-8 -*-

class HomedySpider(scrapy.Spider):
    name = "homedy"
    allowed_domains = ["homedy.com"]
    base_url = "https://homedy.com/ban-can-ho-chung-cu/p"

    def start_requests(self):
        start_urls = [
            "https://homedy.com/ban-can-ho-chung-cu"
        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
        for x in range(1, 201):
            url_page = self.base_url + str(x)
            yield scrapy.Request(url=url_page, callback=self.parse)

    def parse(self, response):
        products = response.css('.tab-content .product-item-top')
        for product in products:
            link_product = product.css('a::attr(href)').extract_first()
            yield response.follow(link_product, self.parse_product)

    def parse_product(self, response):
        item = ItemHomedy()
        item['title'] = response.xpath(
            '/html/body/div[1]/div[5]/div[2]/div[2]/div/div[1]/div/div[1]/div/h1/text()').extract_first()
        try:
            item['price'] = response.xpath(
                '/html/body/div[1]/div[5]/div[2]/div[2]/div/div[1]/div/div[1]/div/div[3]/div[1]/div[1]/strong/span/text()').extract_first() + response.xpath(
                '/html/body/div[1]/div[5]/div[2]/div[2]/div/div[1]/div/div[1]/div/div[3]/div[1]/div[1]/strong/text()').getall()[1]
        except:
            item['price'] = response.xpath(
                '/html/body/div[1]/div[5]/div[2]/div[2]/div/div[1]/div/div[1]/div/div[3]/div[1]/div[1]/strong/span/text()').extract_first()
        item['address'] = response.xpath(
            '/html/body/div[1]/div[5]/div[2]/div[2]/div/div[1]/div/div[1]/div/div[2]/span/text()').getall()
        try:
            item['area'] = response.xpath(
                '/html/body/div[1]/div[5]/div[2]/div[2]/div/div[1]/div/div[1]/div/div[3]/div[1]/div[2]/strong/span/text()').extract_first() + response.xpath(
                '/html/body/div[1]/div[5]/div[2]/div[2]/div/div[1]/div/div[1]/div/div[3]/div[1]/div[2]/strong/text()').getall()[1]
        except:
            item['area'] = response.xpath(
                '/html/body/div[1]/div[5]/div[2]/div[2]/div/div[1]/div/div[1]/div/div[3]/div[1]/div[2]/strong/span/text()').extract_first()
        item['description'] = response.xpath('//*[@id="readmore"]/ul[1]/li/text()').getall()
        item['juridical'] = response.xpath(
            '/html/body/div[1]/div[5]/div[2]/div[2]/div/div[1]/div/div[3]/div[2]/span[2]/text()').extract_first()
        item['type'] = response.xpath(
            '/html/body/div[1]/div[5]/div[2]/div[2]/div/div[1]/div/div[3]/div[1]/span[2]/text()').extract_first()
        item['url_page'] = response.request.url
        item['link_image'] = response.css('body > div.wrapper > div.product > div.image-view img::attr(data-src)').getall()
        item['name_contact'] = response.css('body > div.wrapper > div.product > div.float-in > div.product-item > div > div.md-8 > div > div.agent-inpage > div > div > div.info > div.flex-name > a:nth-child(1) > h3::text').extract_first()
        item['phone_contact'] = response.css('body > div.wrapper > div.product > div.float-in > div.product-item > div > div.md-8 > div > div.agent-inpage > div > div > div.operation > a.btn.tooltip.pc-mobile-number.mobile.mobile-counter.mobile-box::attr(data-mobile)').extract_first()
        yield item