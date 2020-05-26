from crawlinator.items import crawlinatorItem
import scrapy
from loginform import fill_login_form
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import hashlib
class NieuweLoginMetHashSpider(CrawlSpider):
    handle_httpstatus_list = [400, 403, 404, 500, 502, 503, 504]
    name = 'NieuweLoginMetHash'
    allowed_domains = ['onion']
    start_urls = ['http://thestock6nonb74owd6utzh4vld3xsf2n2fwxpwywjgq7maj47mvwmid.onion/viewforum.php?f=18']
    login_url = 'http://thestock6nonb74owd6utzh4vld3xsf2n2fwxpwywjgq7maj47mvwmid.onion/viewtopic.php?f=27&t=733'
    login_password = '34fded6bbd7b816f0ce96544db9bc8df0c30fd1726aa3bec53c060769e104135'
    login_user = 'jonkodonko'
    custom_settings = {
        'LOG_FILE': 'logs/NieuweLoginMetHash.log',
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
        return item 
