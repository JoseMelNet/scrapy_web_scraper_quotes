import time

import scrapy

TITLE_XPATH = '//h1/a/text()'
QUOTES_XPATH = '//span[@class="text" and @itemprop="text"]/text()'
TOP_TEN_TAGS_XPATH = '//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()'
NEXT_PAGE_BUTTON_LINK_XPATH = '//ul[@class="pager"]//li[@class="next"]/a/@href'

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

    def parse_only_quotes(self, response, **kwargs):
        # Receives arguments and append the quotes
        if kwargs:
            # Initializes the list_quotes with quotes obtained at home
            list_quotes = kwargs['quotes']

        # Obtains the quotes in actual page (it could be page2 or page3 or pagen)
        quotes_actual_page = response.xpath(QUOTES_XPATH).getall()
        list_quotes.extend(quotes_actual_page)  # Append the quotes in actual page

        # Verify if the next page exists and then makes a new HTTP request to next page
        next_page_button_link = response.xpath(NEXT_PAGE_BUTTON_LINK_XPATH).get()

        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes,
                                  cb_kwargs={'quotes': list_quotes})
            # Sends to method parse_only_quotes recursively the accumulated quotes in each call to himself
        else:
            # If a next-page doesn't exists then saves an returns the accumulate quotes
            yield {
                'quotes': list_quotes
            }

    def _parse(self, response):
        # Obtains the title, and top_ten_tags in the home 'http://quotes.toscrape.com/'
        title = response.xpath(TITLE_XPATH).get()
        top_ten_tags = response.xpath(TOP_TEN_TAGS_XPATH).getall()
        quotes = response.xpath(QUOTES_XPATH).getall()  # quotes at home

        # Selects the number of tags that I want to obtain
        # top is defined by user in the console
        # The code will be: "scrapy crawl quotes -a top=3"
        # With the before sentence I'll obtain the first three tags
        top = getattr(self, 'top', None)
        if top:
            top = int(top)
            top_tags = top_ten_tags[:top]


        yield {
            'date': date(),
            'title': title,
            'top_tags': top_tags
        }




        # Make a new HTTP request to next page
        next_page_button_link = response.xpath(NEXT_PAGE_BUTTON_LINK_XPATH).get()

        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes})
            # send to method parse_only_quotes the quotes obtained at home
