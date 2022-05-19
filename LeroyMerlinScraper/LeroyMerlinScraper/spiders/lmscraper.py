import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

from LeroyMerlinScraper.items import LeroyMerlinScraperItem


class LeroyMerlinSpider(scrapy.Spider):
    name = 'leroy_goods'
    allowed_domains = ["www.leroymerlin.ro"]
    max_page_number = 3

    def __init__(self, query, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://www.leroymerlin.ro/produse/search/{query}']

    def parse(self, response: TextResponse, page: int = 1, **kwargs):
        print(f'___ PAGE NUMBER {page} ___')
        items_xpath = '//div[@class="col-lg-3 col-md-4 col-sm-4 col-xs-6"]//a[contains(@class, "main-image ' \
                      'data-layer")]/@href'
        next_page_url_xpath = "//a[@class='page-link shadow-sm']/@href"

        urls = response.xpath(items_xpath)
        for i in urls:
            item_url = f'https://www.leroymerlin.ro{i.get()}'
            yield response.follow(item_url, callback=self.parse_item)

        next_page_url = response.xpath(next_page_url_xpath).get()
        if next_page_url and page <= self.max_page_number:
            next_page_url = 'https://www.leroymerlin.ro' + next_page_url
            yield response.follow(next_page_url, callback=self.parse, cb_kwargs={'page': page + 1})

    def parse_item(self, response: TextResponse):
        print('PARSE ITEM')
        # name
        name_xpath = '//h1[@itemprop="name"]/text()'

        # specifications
        table_xpath = "//ul[@class='specification']//li//div//text()"

        # images
        small_imges_xpath = "//ul[@class='row']//img/@src"

        # price
        price_xpath = "//div[@id='store-stock']//div[@class='product_price']//text()"

        loader = ItemLoader(item=LeroyMerlinScraperItem(), response=response)

        loader.add_value("url", response.url)
        loader.add_xpath("name", name_xpath)
        loader.add_xpath("specifications", table_xpath)
        loader.add_xpath("small_images", small_imges_xpath)
        loader.add_xpath("big_images", small_imges_xpath)
        loader.add_xpath("price", price_xpath)

        yield loader.load_item()
