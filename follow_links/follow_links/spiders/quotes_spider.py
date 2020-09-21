import time

import scrapy

TITLE_XPATH = '//h1/a/text()'
QUOTES_XPATH = '//span[@class="text" and @itemprop="text"]/text()'
TOP_TEN_TAGS_XPATH = '//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()'
NEXT_PAGE_BUTTON_LINK_XPATH = '//ul[@class="pager"]//li[@class="next"]/a/@href'


def print_tab():
    print('*' * 10)
    print('\n\n')


def print_items(items_list):
    for item in items_list:
        print(f'- {item}')


def date():
    return (time.asctime(time.localtime()))


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/'
    ]
    custom_settings = {
        'FEED_URI': 'quotes.json',
        'FEED_FORMAT': 'json'
    }

    def _parse(self, response):
        # Obtains the title, quotes and top_ten_tags in the 'http://quotes.toscrape.com/'
        title = response.xpath(TITLE_XPATH).get()
        top_ten_tags = response.xpath(TOP_TEN_TAGS_XPATH).getall()
        quotes = response.xpath(QUOTES_XPATH).getall()

        yield {
            'date': date(),
            'title': title,
            'top_ten_tags': top_ten_tags,
            'quotes': quotes
        }

        # Make a new HTTP request to next page
        next_page_button_link = response.xpath(NEXT_PAGE_BUTTON_LINK_XPATH).get()

        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self._parse)
