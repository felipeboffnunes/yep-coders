import scrapy

class BooksSpider(scrapy.Spider):
    name = 'books_spider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        for book in response.css('article.product_pod'):
            book_url = book.css('h3 a::attr(href)').get()
            yield response.follow(book_url, callback=self.parse_book, meta={'autoextract': {'enabled': True, "pageType": "product"}})

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_book(self, response):
        data = response.meta['autoextract']
        product_data = data.get("product")
        yield product_data
