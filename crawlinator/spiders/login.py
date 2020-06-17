from crawlinator.items import crawlinatorItem
import scrapy
from loginform import fill_login_form
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

import hashlib


class LoginSpider(CrawlSpider):
    handle_httpstatus_list = [400, 403, 404, 500, 502, 503, 504]
    name = 'login'
    # Replace the value with the real domain.
    allowed_domains = ['onion']
    # Replace the value with the website URL to crawl from.
    start_urls = ['http://thestock6nonb74owd6utzh4vld3xsf2n2fwxpwywjgq7maj47mvwmid.onion/viewforum.php?f=18']

    login_url = 'http://thestock6nonb74owd6utzh4vld3xsf2n2fwxpwywjgq7maj47mvwmid.onion/viewtopic.php?f=27&t=733'

    login_user = 'jonkodonko'
    login_password = 'BeepBop0202!HvA'

    custom_settings = {
        'LOG_FILE': 'logs/stock.log',
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
        # let's start by sending a first request to login page
        yield scrapy.Request(self.login_url, self.parse_login)

    def parse_login(self, response):
        # got the login page, let's fill the login form...
        data, url, method = fill_login_form(response.url, response.body, self.login_user, self.login_password)

        # ... and send a request with our login data
        return scrapy.FormRequest(url, formdata=dict(data), method=method, callback=self.start_crawl)

    def start_crawl(self, response):
        # OK, we're in, let's start crawling the protected pages
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
