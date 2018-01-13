from scrapy.spiders import CrawlSpider, Rule
from ..items import *
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings


class Douban_groupSpider(CrawlSpider):
    name = "douban_group"
    allowed_domains = [u'www.douban.com']
    start_urls = [u'https://www.douban.com/group/haixiuzu/discussion']
    rules = (
        Rule(LinkExtractor(allow=('/group/\w+/discussion\?start=[0-9]{0,4}$')), callback='',
        follow=True
        ),
        Rule(LinkExtractor(allow=('/group/topic/\d+/')), callback='parse_topic',
        follow=False
        ),
    )

    def parse_topic(self, response):
        item = TopicItem()
        item['title'] = self.get_title(response)
        item['author'] = self.get_author(response)
        item['description'] = self.get_description(response)
        item['create_time'] = self.get_create_time(response)
        item['image_urls'] = self.get_image_urls(response)
        yield item

    def get_title(self, response):
        title = response.xpath('//title/text()').extract()
        return title[0] if title else ''

    def get_author(self, response):
        author = response.xpath('//div[@class='topic-doc']/h3/span[@class='from']/a/text()').extract()
        return author[0] if author else ''

    def get_description(self, response):
        description = response.xpath('//div[@class='topic-content']').extract()
        return description[0] if description else ''

    def get_create_time(self, response):
        create_time = response.xpath('//div[@class='topic-doc']/h3/span[@class='color-green']/text()').extract()
        return create_time[0] if create_time else ''

    def get_image_urls(self, response):
        image_urls = response.xpath('//div[@class='topic-figure cc']/img/@src').extract()
        return image_urls if image_urls else []

