import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from w3lib.url import url_query_cleaner
import extruct

def process_links(links):
    for link in links:
        link.url = url_query_cleaner(link.url)
        yield link

class ImdbCrawler(CrawlSpider):
    name = 'imdb'
    allowed_domains = ['www.imdb.com']
    start_urls = ['https://www.imdb.com/']
    rules = (
        Rule(
            LinkExtractor(
                deny=[
                    re.escape('https://www.imdb.com/offsite'),
                    re.escape('https://www.imdb.com/whitelist-offsite'),
                ],
            ),
            process_links=process_links,
            callback='parse_item',
            follow=True
        ),
    )

    def parse_item(self, response):
        return {
            'url': response.url,
            'metadata': extruct.extract(
                response.text,
                response.url,
                syntaxes=['opengraph', 'json-ld']
            ),
        }