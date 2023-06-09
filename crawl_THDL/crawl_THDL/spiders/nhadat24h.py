import scrapy
from ..items import ItemNhatdat24h
import time
# -*- coding: utf-8 -*-

class Nhadat24hSpider(scrapy.Spider):
    name = "nhadat24h"
    allowed_domains = ["nhadat24h.net"]
    base_urls = ["https://nhadat24h.net/ban-can-ho-chung-cu"]

    def start_requests(self):
        start_urls = [
            "https://nhadat24h.net/ban-can-ho-chung-cu"
        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        products = response.css('.dv-item')
        for product in products:
            link_product = product.css('a::attr(href)').extract_first()
            yield response.follow(link_product, self.parse_product)
            break

    def parse_product(self, response):
        item = ItemNhatdat24h()
        item['title'] = response.css('.dv-ct-detail > .dv-m-ct-dt > .header > h1::text').extract_first()
        item['price'] = response.xpath(
            '//*[@id="ContentPlaceHolder1_ctl00_lbGiaDienTich"]/label[1]/text()').extract_first() + response.xpath(
            '//*[@id="ContentPlaceHolder1_ctl00_lbGiaDienTich"]/text()[2]').extract_first()
        item['area'] = response.xpath(
            '//*[@id="ContentPlaceHolder1_ctl00_lbGiaDienTich"]/label[2]/text()').extract_first() + response.xpath(
            '//*[@id="ContentPlaceHolder1_ctl00_lbGiaDienTich"]/text()[3]').extract_first()
        item['address'] = response.css('#ContentPlaceHolder1_ctl00_lbTinhThanh::text').extract_first()
        item['description'] = response.css('.dv-txt-mt p::text').getall()
        item['code'] = response.xpath('//*[@id="ContentPlaceHolder1_Panel1"]/div[1]/div[1]/div/div[1]/div[7]/div/table/tbody/tr[2]/td[2]/text()').extract_first()
        item['type'] = response.css('#ContentPlaceHolder1_ctl00_lbLoaiBDS::text').extract_first()
        item['width'] = response.xpath('//*[@id="ContentPlaceHolder1_Panel1"]/div[1]/div[1]/div/div[1]/div[6]/div/table/tbody/tr[2]/td[2]/text()').extract_first()
        item['road_width'] = response.xpath('//*[@id="ContentPlaceHolder1_Panel1"]/div[1]/div[1]/div/div[1]/div[6]/div/table/tbody/tr[1]/td[2]/text()').extract_first()
        item['direct'] = response.xpath('//*[@id="ContentPlaceHolder1_ctl00_lbHuong"]/text()').extract_first()
        item['floor'] = response.xpath('//*[@id="ContentPlaceHolder1_Panel1"]/div[1]/div[1]/div/div[1]/div[5]/div/table/tbody/tr[1]/td[2]/text()').extract_first()
        item['bedroom'] = response.xpath('//*[@id="ContentPlaceHolder1_Panel1"]/div[1]/div[1]/div/div[1]/div[4]/div/table/tbody/tr[1]/td[2]/text()').extract_first()
        item['num_wc'] = response.xpath('//*[@id="ContentPlaceHolder1_Panel1"]/div[1]/div[1]/div/div[1]/div[4]/div/table/tbody/tr[2]/td[2]/text()').extract_first()
        item['parking'] = response.xpath('//*[@id="ContentPlaceHolder1_Panel1"]/div[1]/div[1]/div/div[1]/div[7]/div/table/tbody/tr[1]/td[2]/text()').extract_first()
        item['phone_contact'] = response.xpath('//*[@id="viewmobinumber"]/@href').extract_first()
        item['name_contact'] = response.xpath('//*[@id="ContentPlaceHolder1_Panel1"]/div[1]/div[1]/div/div[2]/div/div[2]/div[1]/div[2]/label[1]/a/text()').extract_first()
        item['url_page'] = response.request.url
        item['link_image'] = response.css('#ContentPlaceHolder1_ctl00_viewImage1_divLi img::attr(data-src)').getall()
        yield item