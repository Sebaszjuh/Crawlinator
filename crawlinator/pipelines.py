# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from elastic_app_search import Client
from scrapy.utils.markup import remove_tags
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
        item['body'] = remove_tags(item['body'])
        return item
