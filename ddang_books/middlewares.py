# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class DdangBooksSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class DdangBooksDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class UserAgentDownloaderMiddleware(object):
    def process_request(self, request, spider):
        request.headers[
            'User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                            'Chrome/77.0.3865.90 Safari/537.36'
        # request.headers['Accept'] = 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, ' \
        #                             'image / apng, * / *;q = 0.8, application / signed - exchange;v = b3 '
        # request.headers['Accept - Encoding'] = 'gzip, deflate'
        # request.headers['Accept - Language'] = 'zh - CN, zh; q = 0.9'
        # request.headers['Connection'] = 'keep - alive'
        # request.headers['Host'] = 'category.dangdang.com'
        # request.headers['Upgrade - Insecure - Requests'] = '1'
        # if request.headers['Referer'] == None:
        # request.headers['Referer'] = 'http://book.dangdang.com'
        # request.headers['Cookies'] = '__permanent_id = 20190921204056994185480722080470392;NTKF_T2D_CLIENTID = ' \
        #                              'guestE3113965 - 8211 - B722 - 2ACB - 53D726CEED28;ddscreen = 2;producthistoryid ' \
        #                              '= 25090502 % 2C1513768139 % 2C1468588027 % 2C1468824227 % 2C24156030 % ' \
        #                              '2C23677431;nTalk_CACHE_DATA = {uid: dd_1000_ISME9754_guestE3113965 - 8211 - B7, ' \
        #                              'tid: 1571459519432231};dest_area = country_id % 3D9000 % 26province_id % 3D111 ' \
        #                              '% 26city_id % 3D0 % 26district_id % 3D0 % 26town_id % 3D0; '



