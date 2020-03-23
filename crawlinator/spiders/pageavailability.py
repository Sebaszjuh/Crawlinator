from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from crawlinator.items import crawlinatorItem


class PageavailabilitySpider(CrawlSpider):
    handle_httpstatus_list = [400, 403, 404, 500, 502, 503, 504]
    name = 'davidsoff'
    # Replace the value with the real domain.
    allowed_domains = ['davidsoff.nl']
    # Replace the value with the website URL to crawl from.
    start_urls = ['http://www.davidsoff.nl']
    custom_settings = {
        'LOG_FILE': 'logs/pageavailability.log',
        'LOG_LEVEL': 'INFO'
    }

    rules = (
        Rule(
            LinkExtractor(
                tags='a',
                attrs='href',
                unique=True
            ),
            callback='parse_item',
            follow=True
        ),
    )

    def parse_item(self, response):
        item = crawlinatorItem()
        item['title'] = response.css('title::text').extract_first()
        item['url'] = response.url
        item['status'] = response.status
        return item
