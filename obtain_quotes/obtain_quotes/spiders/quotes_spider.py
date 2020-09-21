import scrapy

TITLE_XPATH = '//h1/a/text()'
QUOTES_XPATH = '//span[@class="text" and @itemprop="text"]/text()'
TOP_TEN_TAGS_XPATH = '//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()'

def tab():
    print('*' * 10)
    print('\n\n')

def print_items(items_list):
    for item in items_list:
        print(f'- {item}')


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/'
    ]


    def _parse(self, response):

        tab()
        title = response.xpath(TITLE_XPATH).get()
        print(f'Title: {title}')
        tab()

        tab()
        quotes = response.xpath(QUOTES_XPATH).getall()
        print(f'Quotes: ')
        print_items(quotes)
        tab()

        tab()
        top_ten_tags = response.xpath(TOP_TEN_TAGS_XPATH).getall()
        print('Top Ten Tags: ')
        print_items(top_ten_tags)
        tab()





