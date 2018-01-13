import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from douban_group.spiders.douban_group import Douban_groupSpider


process = CrawlerProcess(get_project_settings())
process.crawl(Douban_groupSpider)
process.start()
