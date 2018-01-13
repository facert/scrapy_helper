from scrapy.spiders import CrawlSpider, Rule
from ..items import *
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings


class ${project.name.capitalize()}Spider(CrawlSpider):
    name = "${project.name}"
    allowed_domains = ${project.domain.split(",")}
    start_urls = ${project.start_urls.split(",")}
    rules = (
        % for rule_field in rule_fields:
        Rule(LinkExtractor(allow=('${rule_field["rule"].path}')), callback='${rule_field["rule"].callback_func}',
        % if rule_field['rule'].callback_func:
        follow=False
        % else:
        follow=True
        % endif
        ),
        % endfor
    )

    % for rule_field in rule_fields:
    % if rule_field['rule'].callback_func:
    def ${rule_field["rule"].callback_func}(self, response):
        item = ${rule_field["rule"].callback_func.split("_")[-1].capitalize()}Item()
        % for field in rule_field["fields"]:
        item['${field.name}'] = self.get_${field.name}(response)
        % endfor
        yield item
    % endif
    % endfor

    % for field in rule_field["fields"]:
    % if field.name == "image_urls":
    def get_${field.name}(self, response):
        ${field.name} = response.xpath('${field.path}').extract()
        return ${field.name} if ${field.name} else []
    % else:
    def get_${field.name}(self, response):
        ${field.name} = response.xpath('${field.path}').extract()
        return ${field.name}[0] if ${field.name} else ''
    % endif

    % endfor