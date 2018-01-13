import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from jiandan.spiders.jiandan import JiandanSpider


process = CrawlerProcess(get_project_settings())
process.crawl(JiandanSpider)
process.start()
