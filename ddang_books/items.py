# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from datetime import datetime
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose


def get_num_from_str(value):
    '''
    将字符串类型的数字转换成数字
    :param num_str:字符串类型数字，可能包含"万"或"+"或"万+"
    :return:成功返回数字，默认返回0
    '''
    num = 0
    num_str = re.search(r'\D*(\d+\.?\d*).*', value).group(1)
    if "." in num_str:
        num = float(num_str)
    else:
        num = int(num_str)
    if "万" in value:
        num = num * 10000
    return num

def exec_strip(value):
    return value.strip()

def get_date_str(value):
    ma = re.match('\D*(\d{0,4}\-\d{0,2}\-\d{0,2}).*',value)
    if ma:
        return ma.group(1)

def format_date(value):
    try:
        f_t = datetime.strptime(value, '%Y-%m-%d')
    except Exception as e:
        f_t = datetime.date()
    return f_t

def return_value(value):
    return value

def convert_star_num(value):
    star_perc = re.match('\D+(\d{1,3})%.*', value).group(1)
    star_nums = {
        '100': 5,
        '90': 4.5,
        '80': 4,
        '70': 3.5,
        '60': 3,
        '50': 2.5,
        '40': 2,
        '30': 1.5,
        '20': 1,
        '10': 0.5,
        '0': 0,
    }
    return float(star_nums[star_perc])

# def add_space_to_none(value):
#     if not value:
#         return value.append(" ")
#     return value

class BookItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

class DdangBooksItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    id = scrapy.Field(
        input_processor = MapCompose(get_num_from_str)
    )
    name = scrapy.Field(
        input_processor = MapCompose(exec_strip)
    )
    image_url = scrapy.Field(
        # 用于覆盖TakeFirst(),输出传入的原始value[image_url]，否则为一字符串，会在pipeline的get_media_requests中报错
        output_processor=MapCompose(return_value)
    )
    author = scrapy.Field(
        input_processor = MapCompose(exec_strip)
    )
    price = scrapy.Field(
        input_processor = MapCompose(get_num_from_str)
    )
    publisher = scrapy.Field(
        input_processor = MapCompose(exec_strip)
    )
    pub_time = scrapy.Field(
        input_processor = MapCompose(exec_strip, get_date_str, format_date)
    )
    title = scrapy.Field(
        input_processor = MapCompose(exec_strip)
    )
    comment_nums = scrapy.Field(
        input_processor = MapCompose(exec_strip, get_num_from_str)
    )
    star_level = scrapy.Field(
        input_processor = MapCompose(convert_star_num)
    )
    category_1 = scrapy.Field()
    category_2 = scrapy.Field()
    category_3 = scrapy.Field()
    book_url = scrapy.Field()
    image_alt = scrapy.Field(
        input_processor = MapCompose(exec_strip)
    )

    def get_insert_mysql(self):
        insert_sql = """
            insert into ddangbooks(id, name, image_url, author, price, publisher, pub_time, title, comment_nums, star_level,
                    category_1, category_2, category_3, book_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE price=VALUES(price), comment_nums=VALUES(comment_nums), star_level=VALUES(star_level)
            """
        params = (
            self['id'], self['name'], self['image_url'], self['author'], self['price'], self['publisher'], self['pub_time'], self['title'],
            self['comment_nums'], self['star_level'], self['category_1'], self['category_2'], self['category_3'], self['book_url']
        )
        return insert_sql, params