import scrapy

class BooksSpider(scrapy.Spider):
    name = 'books_spider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    custom_settings = {
        "ZYTE_API_TRANSPARENT_MODE": True,
    }

    def parse(self, response):
        for book in response.css('article.product_pod'):
            book_url = book.css('h3 a::attr(href)').get()
            yield response.follow(book_url, callback=self.parse_book)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_book(self, response):
        product = response.css("div.product_main")
        title = product.css("h1::text").get()
        price = product.css("p.price_color::text").get()
        availability = product.css("p.availability ::text").getall()
        if availability:
            availability = "".join(availability).strip()
        rating = product.css("p.star-rating::attr(class)").get()
        if rating:
            rating = rating.replace("star-rating", "")

        yield {
            "title": title,
            "price": price,
            "availability": availability,
            "rating": rating
        }
