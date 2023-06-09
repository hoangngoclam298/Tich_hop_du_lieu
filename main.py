from crawl_THDL.crawl_THDL.spiders.alonhadat import AlonhadatSpider
from scrapy.crawler import CrawlerProcess

process = CrawlerProcess()
process.crawl(AlonhadatSpider)


