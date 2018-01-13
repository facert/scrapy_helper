import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from chuansong.spiders.chuansong import ChuansongSpider


process = CrawlerProcess(get_project_settings())
process.crawl(ChuansongSpider)
process.start()
