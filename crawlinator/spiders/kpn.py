from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from crawlinator.items import crawlinatorItem
import hashlib
class kpnSpider(CrawlSpider):
    handle_httpstatus_list = [400, 403, 404, 500, 502, 503, 504]
    name = 'kpn'
    allowed_domains = ['https://www.kpn.com/']
    start_urls = ['https://www.kpn.com/']
    custom_settings = {
        'LOG_FILE': 'logs/kpn.log',
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
        item['id'] = hashlib.sha256(response.url.encode('utf-8')).hexdigest()
        item['title'] = response.css('title::text').extract_first()
        item['url'] = response.url
        item['status'] = response.status
        item['body'] = response.text
        return item