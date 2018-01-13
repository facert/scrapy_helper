from scrapy.spiders import CrawlSpider, Rule
from ..items import *
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings


class ZiroomSpider(CrawlSpider):
    name = "ziroom"
    allowed_domains = [u'www.ziroom.com']
    start_urls = [u'http://www.ziroom.com/z/nl/z2-d23008614.html']
    rules = (
        Rule(LinkExtractor(allow=('/z/nl/z2-\d+\.html?p=\d+')), callback='',
        follow=True
        ),
        Rule(LinkExtractor(allow=('/z/vr/\d+\.html')), callback='parse_room',
        follow=False
        ),
    )

    def parse_room(self, response):
        item = RoomItem()
        item['name'] = self.get_name(response)
        item['price'] = self.get_price(response)
        item['ellipsis'] = self.get_ellipsis(response)
        yield item

    def get_name(self, response):
        name = response.xpath('//div[@class="room_name"]/h2/text()').extract()
        return name[0] if name else ''

    def get_price(self, response):
        price = response.xpath('//span[@class="room_price"]/text()').extract()
        return price[0] if price else ''

    def get_ellipsis(self, response):
        ellipsis = response.xpath('//span[@class="ellipsis"]/text()').extract()
        return ellipsis[0] if ellipsis else ''

