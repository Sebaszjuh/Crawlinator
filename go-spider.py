from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from crawlinator.spiders.ziggo import ZiggoSpider
from crawlinator.spiders.tor import TorSpider
from crawlinator.spiders.login import LoginSpider


process = CrawlerProcess(get_project_settings())
process.crawl(LoginSpider)
process.start()
