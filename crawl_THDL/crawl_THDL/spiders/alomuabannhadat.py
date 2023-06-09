import scrapy
from ..items import ItemAlomuabannhadat
import time
import regex as re
# -*- coding: utf-8 -*-

def check_date(text):
    # Sử dụng biểu thức chính quy để tìm kiếm ngày trong văn bản
    pattern = r"\b(\d{1,2}-\d{1,2}-\d{4})\b"
    matches = re.findall(pattern, text)
    return matches

class AlomuabannhadatSpider(scrapy.Spider):
    name = "alomuabannhadat"
    allowed_domains = ["alomuabannhadat.vn"]
    base_url = "https://alomuabannhadat.vn/nha-ban/ban-can-ho-chung-cu/page-"

    def start_requests(self):
        start_urls = [
            "https://alomuabannhadat.vn/nha-ban/ban-can-ho-chung-cu/"
        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
        for x in range(1, 120):
            url_page = self.base_url + str(x)
            yield scrapy.Request(url=url_page, callback=self.parse)

    def parse(self, response):
        products = response.css('.wrap-property > .property')
        for product in products:
            link_product = product.css('.info > a::attr(href)').extract_first()
            yield scrapy.Request(link_product, self.parse_product)

    def parse_product(self, response):
        item = ItemAlomuabannhadat()
        item['title'] = response.css('#property-detail h1::text').extract_first()
        item['price'] = response.xpath(
            '//*[@id="quick-summary"]/dl/dd[2]/span/text()').extract_first()
        item['address'] = response.xpath('//*[@id="quick-summary"]/dl/dd[3]/text()').extract_first()
        item['area'] = response.xpath('//*[@id="quick-summary"]/dl/dd[4]/text()').extract_first()
        if(len(check_date(response.xpath('//*[@id="quick-summary"]/dl/dd[7]').extract_first())) > 0):
            item['date'] = check_date(response.xpath('//*[@id="quick-summary"]/dl/dd[7]').extract_first())[0]
        else:
            item['date'] = check_date(response.xpath('//*[@id="quick-summary"]/dl/dd[6]').extract_first())[0]
        item['description'] = response.xpath('//*[@id="description"]/p/text()').extract()
        item['code'] = response.xpath('//*[@id="quick-summary"]/dl/dd[1]/text()').extract_first()
        item['features'] = response.xpath('//*[@id="property-features"]/ul//li//text()').getall()
        '//*[@id="quick-summary"]/dl/dd[7]'
        if(response.xpath('//*[@id="quick-summary"]/dl/dd[8]/text()').extract_first() != None):
            item['name_contact'] = response.xpath('//*[@id="quick-summary"]/dl/dd[8]/text()').extract_first()
        else:
            item['name_contact'] = response.xpath('//*[@id="quick-summary"]/dl/dd[7]/text()').extract_first()
        if(response.xpath('//*[@id="quick-summary"]/dl/dd[9]/b/a//@onclick').extract_first() != None):
            item['phone_contact'] = response.xpath('//*[@id="quick-summary"]/dl/dd[9]/b/a//@onclick').extract_first()
        else:
            item['phone_contact'] = response.xpath('//*[@id="quick-summary"]/dl/dd[8]/b/a//@onclick').extract_first()
        item['url_page'] = response.request.url
        item['link_image'] = response.css('#property-gallery img::attr(src)').getall()
        yield item
