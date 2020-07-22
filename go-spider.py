from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from crawlinator.spiders.tor import TorSpider

process = CrawlerProcess(get_project_settings())
process.crawl(TorSpider)
process.start()
