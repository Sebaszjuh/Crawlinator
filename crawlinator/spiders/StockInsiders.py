from crawlinator.items import crawlinatorItem
import scrapy
from loginform import fill_login_form
from scrapy.linkextractors import LinkExtractor
from datetime import datetime
import urllib
from scrapy.spiders import CrawlSpider, Rule
import hashlib
class StockInsidersSpider(CrawlSpider):
    handle_httpstatus_list = [400, 403, 404, 500, 502, 503, 504]
    name = 'StockInsiders'
    allowed_domains = ['onion']
    start_urls = ['http://thestock6nonb74owd6utzh4vld3xsf2n2fwxpwywjgq7maj47mvwmid.onion/']
    login_url = 'http://thestock6nonb74owd6utzh4vld3xsf2n2fwxpwywjgq7maj47mvwmid.onion/ucp.php?mode=login'
    hashed_login_password = '3c1ba8e9971f7cd3b2433e52bac80dc0641490e745ff86bc77b7faa711da0217d28dd45dfe08a8c6bf86fc5b4881224420d8935a6bd4ed78d640f75c6abd475e'
    login_user = 'jonkodonko'
    custom_settings = {
        'LOG_FILE': 'logs/StockInsiders.log',
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
    def start_requests(self):
        yield scrapy.Request(self.login_url, self.parse_login)
    def parse_login(self, response):
        data, url, method = fill_login_form(response.url, response.body, self.login_user, self.login_password)
        return scrapy.FormRequest(url, formdata=dict(data), method=method, callback=self.start_crawl)
    def start_crawl(self, response):
        for url in self.start_urls:
            yield scrapy.Request(url)
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
