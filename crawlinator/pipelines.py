# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from elastic_app_search import Client
from scrapy.utils.markup import replace_tags, remove_tags_with_content, replace_escape_chars
from scrapy.selector import Selector
import logging
class appSearchPipeline(object):
    def process_item(self, item, spider):

        client = Client(
            base_endpoint='localhost:3002/api/as/v1',
            api_key='private-p1j1xmt5gu33bdyjd5c4ipj6',
            use_https=False
        )
        engine_name = 'crawlinator'
        client.index_document(engine_name, dict(item))
        logging.info(f'Item sent to App Search: {item["title"]}')
        return item

class bodyCleanupPipeline(object):

    def process_item(self, item, spider):
        body_only = Selector(text=item['body']).css('body').get()
        script_removed = remove_tags_with_content(body_only, which_ones=('style', 'script'))
        tags_replaced = replace_tags(script_removed, ' ')
        item['body'] = replace_escape_chars(tags_replaced, ' ')

        logging.info(f'Item cleaned up: {item["title"]}')
        return item
