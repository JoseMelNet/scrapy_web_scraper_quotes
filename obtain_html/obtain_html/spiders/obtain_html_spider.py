import scrapy

class Quotes_Spider(scrapy.Spider):
    name = 'obtain_html'
    start_urls = [
        'http://quotes.toscrape.com/'
    ]

    def parse(self, response):
        with open('results.html', 'w', encoding='utf-8') as f:
            f.write(response.text)