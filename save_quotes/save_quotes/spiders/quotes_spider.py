import scrapy

TITLE_XPATH = '//h1/a/text()'
QUOTES_XPATH = '//span[@class="text" and @itemprop="text"]/text()'
TOP_TEN_TAGS_XPATH = '//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()'

def print_tab():
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

        title = response.xpath(TITLE_XPATH).get()
        quotes = response.xpath(QUOTES_XPATH).getall()
        top_ten_tags = response.xpath(TOP_TEN_TAGS_XPATH).getall()

        yield{
            'title': title,
            'quotes': quotes,
            'top_ten_tags': top_ten_tags
        }