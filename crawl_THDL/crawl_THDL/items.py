# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class CrawlThdlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ItemAlonhadat(scrapy.Item):
    title = Field()
    price = Field()
    square = Field()
    project = Field()
    description = Field()
    road_width = Field()
    floor = Field()
    bedroom = Field()
    kitchen = Field()
    diningroom = Field()
    terrace = Field()
    parking = Field()
    direct = Field()
    address = Field()
    date = Field()
    width = Field()
    length = Field()
    code = Field()
    type = Field()
    juridical = Field()
    link_image = Field()
    name_contact = Field()
    phone_contact = Field()
    introduce_contact = Field()
    url_page = Field()

class ItemIbatdongsan(scrapy.Item):
    title = Field()
    price = Field()
    address = Field()
    area = Field()
    date = Field()
    description = Field()
    code = Field()
    type = Field()
    width = Field()
    length = Field()
    direct = Field()
    road_width = Field()
    juridical = Field()
    floor = Field()
    bedroom = Field()
    kitchen = Field()
    diningroom = Field()
    terrace = Field()
    parking = Field()
    phone_contact = Field()
    name_contact = Field()
    link_image = Field()
    url_page = Field()

class ItemAlomuabannhadat(scrapy.Item):
    title = Field()
    price = Field()
    address = Field()
    area = Field()
    date = Field()
    description = Field()
    code = Field()
    features = Field()
    phone_contact = Field()
    name_contact = Field()
    link_image = Field()
    url_page = Field()
