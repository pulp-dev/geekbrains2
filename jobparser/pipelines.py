# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pymongo import MongoClient
from itemadapter import ItemAdapter

import re


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

    def delete_all(self, spider):
        self.db[spider.name].drop()

    def mongo_pipeline(self, item, spider):
        mongo_params = self.from_crawler(spider)
        self.mongo_uri = mongo_params.mongo_uri
        self.mongo_db = mongo_params.mongo_db
        self.open_spider(spider)
        self.insert_item(item, spider)
        self.close_spider(spider)


class JobparserPipeline(MongoPipeline):

    def process_salary(self, salary_list: list):
        if len(salary_list) == 1:
            return None, None, None
        elif len(salary_list) == 3:
            salary_min = None
            salary_max = salary_list[2][:-4].strip()
            currency = salary_list[2][-4:]
        else:
            try:
                salary_min = salary_list[1]
                salary_max = salary_list[3]
                currency = salary_list[5]
            except IndexError:
                salary_max = salary_list[1]
                currency = salary_list[3]
                salary_min = None

        return salary_min, salary_max, currency

    def process_item(self, item, spider):
        s_min, s_max, s_currency = self.process_salary(item["salary"])
        item["title"] = " ".join(item["title"])
        print(item['title'])
        if s_min:
            item["salary_min"] = s_min
        if s_max:
            item["salary_max"] = s_max
        if s_currency:
            item["salary_currency"] = s_currency
        # del item['salary']
        item.pop("salary")

        self.mongo_pipeline(item, spider)
        print('___ ITEM HAS BEEN INSERTED ___')

        return item
