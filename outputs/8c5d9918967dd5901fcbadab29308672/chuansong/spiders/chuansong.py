from scrapy.spiders import CrawlSpider, Rule
from ..items import *
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings


class ChuansongSpider(CrawlSpider):
    name = "chuansong"
    allowed_domains = [u'chuansong.me']
    start_urls = [u'http://chuansong.me/']
    rules = (
        Rule(LinkExtractor(allow=('/\?start=\d+')), callback='',
        follow=True
        ),
        Rule(LinkExtractor(allow=('/n/\d+')), callback='parse_article',
        follow=False
        ),
    )

    def parse_article(self, response):
        item = ArticleItem()
        item['title'] = self.get_title(response)
        item['post_date'] = self.get_post_date(response)
        item['post_user'] = self.get_post_user(response)
        item['post_user_link'] = self.get_post_user_link(response)
        yield item

    def get_title(self, response):
        title = response.xpath('//h2[@id="activity-name"]/text()').extract()
        return title[0] if title else ''

    def get_post_date(self, response):
        post_date = response.xpath('//em[@id="post-date"]/text()').extract()
        return post_date[0] if post_date else ''

    def get_post_user(self, response):
        post_user = response.xpath('//a[@id="post-user"]/text()').extract()
        return post_user[0] if post_user else ''

    def get_post_user_link(self, response):
        post_user_link = response.xpath('//a[@id="post-user"]/@href').extract()
        return post_user_link[0] if post_user_link else ''

