from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from crawlinator.items import crawlinatorItem
from datetime import datetime
import urllib
import hashlib
class testSpider(CrawlSpider):
    handle_httpstatus_list = [400, 403, 404, 500, 502, 503, 504]
    name = 'test'
    start_urls = ['https://test.nl/']
    custom_settings = {
        'LOG_FILE': 'logs/test.log',
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
        item['date'] = datetime.today().strftime('%d/%m/%Y')
        item['time'] = datetime.today().strftime('%H:%M:%S')
        item['datetime'] = item['date'] + ', ' + item['time']
        item['threat'] = list(set([
            word.lower()
            for word in self.threat_keywords()
            if response.xpath('//*[contains(text(),"%s")]' % word)
        ]))
        return item
    def make_usable_url(self, url):
        split = urllib.parse.urlsplit(url)
        split = split._replace(netloc=f'{split.netloc}.sh')
        return urllib.parse.urlunsplit(split)
    def threat_keywords(self):
        keywords = []
        for word in open('keyword-list.txt', 'r'):
            keywords.append(word.rstrip('\n'))
        return keywords
