import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from ${project.name}.spiders.${project.name} import ${project.name.capitalize()}Spider


process = CrawlerProcess(get_project_settings())
process.crawl(${project.name.capitalize()}Spider)
process.start()
