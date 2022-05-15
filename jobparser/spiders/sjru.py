import scrapy
from scrapy.http import TextResponse

from jobparser.items import JobparserItem

TEMPLATE_URL = 'https://russia.superjob.ru/vacancy/search/?keywords='


class SuperJobSpider(scrapy.Spider):
    name = 'sjru'
    max_page_number = 2

    def __init__(self, query, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [TEMPLATE_URL + query]

    def parse_item(self, response: TextResponse):
        print('___ PARSE ITEM ___')
        title_xpath = "//h1[@class='KySx7 Oert7 _2APER Q0JS1 _2L5ou _1TcZY Bbtm8']/text()"
        salary_xpath = "//span[@class='_2eYAG -gENC _1TcZY dAWx1']/text()"

        title = response.xpath(title_xpath).get()
        if title == None:
            print('___ ADVERTISEMENT WAS SKIPPED ___')
            print(response.url)
            return
        salary = response.xpath(salary_xpath).getall()

        item = JobparserItem()
        item['title'] = [title]
        item['salary'] = salary
        item['url'] = response.url
        yield item

    def parse(self, response: TextResponse, page: int = 1, **kwargs):
        for i in range(self.max_page_number):
            print(f"___ PAGE_NUMBER: {page} ___")

            _ = response.xpath("//div[@class='f-test-search-result-item']")
            items_urls = _.xpath('.//a[contains(@class, "_2b9za f-test-link")]/@href')
            next_page_url_xpath = "//a[contains(@class, 'f-test-button-dalshe')]//@href"

            for i in items_urls:
                url = i.get()
                yield response.follow(url, callback=self.parse_item)

            next_page_url = response.xpath(next_page_url_xpath).get()
            if next_page_url and page < self.max_page_number:
                next_page_url = 'https://russia.superjob.ru' + next_page_url
                yield response.follow(next_page_url, callback=self.parse, cb_kwargs={'page': page + 1})
