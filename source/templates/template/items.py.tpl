
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


% for rule_field in rule_fields:
% if rule_field["rule"].callback_func:
class ${rule_field["rule"].callback_func.split("_")[-1].capitalize()}Item(scrapy.Item):
    % for field in rule_field["fields"]:
    ${field.name} = scrapy.Field()
    % endfor
% endif
% endfor
