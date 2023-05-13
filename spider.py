import scrapy

class MySpider(scrapy.Spider):
    name = "myspider"
    start_urls = ["https://batdongsan.com.vn/nha-dat-ban/p1"]

    def parse(self, response):
        # Tìm các thẻ <a> trên trang web
        for link in response.css('a'):
            # Lấy URL và tiêu đề của trang web liên kết
            url = link.css('::attr(href)').extract_first()
            title = link.css('::text').extract_first()

            # Nếu có URL và tiêu đề thì lưu vào đối tượng Item
            if url and title:
                yield {'url': url, 'title': title}