import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from ziroom.spiders.ziroom import ZiroomSpider


process = CrawlerProcess(get_project_settings())
process.crawl(ZiroomSpider)
process.start()
