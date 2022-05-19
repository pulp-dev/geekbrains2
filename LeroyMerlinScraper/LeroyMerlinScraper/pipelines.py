# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib
from scrapy.utils.python import to_bytes

from pymongo import MongoClient
from itemadapter import ItemAdapter

import scrapy

from scrapy.pipelines.images import ImagesPipeline


class MongoPipeline:

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def insert_item(self, item, spider):
        self.db[spider.name].update_one(
            {'url': item['url']},
            {
                '$set': ItemAdapter(item).asdict()
            },
            upsert=True
        )
        return item

    def delete_all(self, spider, sure=False):
        if sure:
            self.db[spider.name].drop()
            print('collection fully deleted')
            return
        print('not sure')

    def mongo_pipeline(self, item, spider):
        mongo_params = self.from_crawler(spider)
        self.mongo_uri = mongo_params.mongo_uri
        self.mongo_db = mongo_params.mongo_db
        self.open_spider(spider)
        self.insert_item(item, spider)
        self.close_spider(spider)
        print('___ ITEM HAS BEEN SUCCESSFULLY INSERTED INTO DB ___')


class LeroyMerlinScraperPipeline(MongoPipeline):
    def process_item(self, item, spider):
        print("PROCESS ITEM")
        self.mongo_pipeline(item, spider)
        return item


class LeroyMerlinScraperImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item["small_images"] and item['big_images']:
            for img_url in item['small_images']:
                try:
                    yield scrapy.Request(img_url)
                    i = item['small_images'].index(img_url)
                    yield scrapy.Request(item['big_images'][i])
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        print('ITEM COMPLETED')
        if results:
            item['img_info'] = [r[1] for r in results if r[0]]
            del item['small_images']
            del item['big_images']
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        return f'{item["url"].split("/")[-1]}/{item["name"]}.jpg'
