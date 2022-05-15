from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser.spiders.sjru import SuperJobSpider
from jobparser import settings
from jobparser.spiders.hhru import HhruSpider

if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)

    query = input('Искомая профессия - ')

    common_kwargs = {"query": query}
    # process.crawl(HhruSpider, **common_kwargs)

    print('___ SuperJob ___')
    process.crawl(SuperJobSpider, **common_kwargs)

    process.start()

    print('___ PROCESS FINISHED ___')
