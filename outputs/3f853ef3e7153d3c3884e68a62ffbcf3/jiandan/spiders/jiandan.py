from scrapy.spiders import CrawlSpider, Rule
from ..items import *
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings


class JiandanSpider(CrawlSpider):
    name = "jiandan"
    allowed_domains = [u'jandan.net']
    start_urls = [u'http://jandan.net/ooxx']
    rules = (
        Rule(LinkExtractor(allow=('/ooxx/page-\d+#comments')), callback='parse_image',
        follow=False
        ),
    )

    def parse_image(self, response):
        item = ImageItem()
        item['image_urls'] = self.get_image_urls(response)
        yield item

    def get_image_urls(self, response):
        image_urls = response.xpath('//a[@class="view_img_link"]/@href').extract()
        return image_urls if image_urls else []

