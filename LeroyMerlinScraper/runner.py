import requests

from urllib import parse

import scrapy
from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

from LeroyMerlinScraper import settings
from LeroyMerlinScraper.spiders.lmscraper import LeroyMerlinSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)

    query = input('Искомый товар - ')
    query = parse.quote_plus(query.encode("utf-8"))
    kwargs = {'query': query}

    process.crawl(LeroyMerlinSpider, **kwargs)
    process.start()
