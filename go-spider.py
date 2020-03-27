from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from crawlinator.spiders.davidsoff import DavidSoffSpider
from crawlinator.spiders.ziggo import ZiggoSpider
from crawlinator.spiders.tortest import TorSpider


process = CrawlerProcess(get_project_settings())
process.crawl(TorSpider)
process.start()
