import scrapy
from scrapy import Request
from scrapy.http import TextResponse


# from LeroyMerlinScraper.LeroyMerlinScraper.items import


class LeroyMerlinSpider(scrapy.Spider):
    name = 'lmscraper'
    allowed_domains = ["www.leroymerlin.ro"]
    max_page_number = 3

    def __init__(self, query, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://www.leroymerlin.ro/produse/search/{query}']

    def parse(self, response: TextResponse, page: int = 1, **kwargs):
        items_xpath = '//div[@class="col-lg-3 col-md-4 col-sm-4 col-xs-6"]//a[contains(@class, "main-image ' \
                      'data-layer")]/@href'
        urls = response.xpath(items_xpath)
        for i in urls:
            item_url = f'https://www.leroymerlin.ro{i.get()}'
            yield response.follow(item_url, callback=self.parse_item)

    def parse_item(self, response: TextResponse):
        print('PARSE ITEM')
        # name
        name_xpath = '//h1[@itemprop="name"]/text()'
        name = response.xpath(name_xpath).get()

        # specifications
        table_xpath = "//ul[@class='specification']//li"
        table = response.xpath(table_xpath)
        specifications = {}
        for cell in table:
            label = cell.xpath('.//div//text()')
            specifications[label.getall()[0].replace(' ', '').replace('\n', '')] = \
                label.getall()[1].replace(' ', '').replace('\n', '')
            print()

        # images
        small_imges_xpath = "//ul[@class='row']//img/@src"
        re_imges = response.xpath(small_imges_xpath).getall()
        big_imges = []
        for img in re_imges:
            big_imges.append(img.replace('/500/500', '/2000/2000'))

        # price
        price_xpath = "//div[@id='store-stock']//div[@class='product_price']"
        price = response.xpath(price_xpath + '/text()').get().replace(' ', '').replace('\n', '').replace(',', '.') + \
                response.xpath(price_xpath + '/sub/text()').get().replace(' ', '').replace('\n', '')
        price = float(price)

        print()
