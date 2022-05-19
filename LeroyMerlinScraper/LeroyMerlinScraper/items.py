# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Compose, MapCompose, TakeFirst


def normalize_name(name: str):
    return name.replace('\n', '').replace(' ', '')


def normalize_strings_in_table(cell: str):
    return cell.replace('\n', '').replace(' ', '')


def get_table_from_list(cells_array: list):
    cells_array = list(map(normalize_strings_in_table, cells_array))
    for cell in cells_array:
        if cell == '':
            cells_array.pop(cells_array.index(cell))

    table = []
    for i in range(0, len(cells_array), 2):
        s = cells_array[i] + ': ' + cells_array[i + 1]
        table.append(s)

    return table


def get_big_images_urls(img_url: str):
    return img_url.replace('/500/500', '/2000/2000')


def get_full_price(price_parts_list: list):
    price = price_parts_list[0].replace(' ', '').replace('\n', '').replace(',', '.') + \
            price_parts_list[1].replace(' ', '').replace('\n', '')
    return float(price)


class LeroyMerlinScraperItem(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(input_processor=MapCompose(normalize_name), output_processor=TakeFirst())
    specifications = scrapy.Field(input_processor=Compose(get_table_from_list))
    small_images = scrapy.Field()
    big_images = scrapy.Field(input_processor=MapCompose(get_big_images_urls))
    price = scrapy.Field(input_processor=Compose(get_full_price), output_processor=TakeFirst())
    img_info = scrapy.Field()
