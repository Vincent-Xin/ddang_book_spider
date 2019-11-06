# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re

from pymysql import cursors
from scrapy.http import Request
from scrapy.pipelines.images import ImagesPipeline
from twisted.enterprise import adbapi


class DdangBooksPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        params = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            cursorclass=cursors.DictCursor,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **params)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 利用连接池对象，开始操作数据，将数据写入到数据库中
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 如果异步任务执行失败的话，可以通过ErrBack()进行监听, 给insert_db添加一个执行失败的回调事件
        query.addErrback(self.handle_error, item, spider)

        return item

    def handle_error(self, failure, item, spider):
        print('-----数据库写入失败', failure)

    def do_insert(self, cursor, item):
        insert_sql, params = item.get_insert_mysql()
        cursor.execute(insert_sql, params)


class ImageDownloaderPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        # image_url = item.get('image_url', "")
        return [Request(url=item.get('image_url', "")[0], meta={'item': item})]

    # def item_completed(self, results, item, info):
    #     if isinstance(item, dict) or self.images_result_field in item.fields:
    #         item[self.images_result_field] = [x for ok, x in results if ok]
    #     return item

    def file_path(self, request, response=None, info=None):
        # image_item = self.item_completed()
        image_item = request.meta['item']
        image_level_1, image_level_2, image_level_3 = image_item['category_1'].replace('/', '-'), image_item['category_2'].replace('/', '-'), image_item['category_3'].replace('/', '-')
        image_num_name = re.search('.*ddimg\.cn/.+/(\d+\-.+)\.jpg', request.url).group(1)
        image_name = image_num_name or image_item['image_alt'] or image_item['name']
        if image_level_2 == " ":
            return '%s/%s.jpg' % (image_level_1, image_name)
        elif image_level_3 == " ":
            return '%s/%s/%s.jpg' % (image_level_1, image_level_2, image_name)
        return '%s/%s/%s/%s.jpg' % (image_level_1, image_level_2, image_level_3, image_name)
