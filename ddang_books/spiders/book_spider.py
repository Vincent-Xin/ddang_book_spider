# -*- coding: utf-8 -*-
import re
from urllib import parse

import scrapy
from scrapy.http import Request

from ddang_books.items import DdangBooksItem, BookItemLoader


class BookSpiderSpider(scrapy.Spider):
    name = 'book_spider'
    allowed_domains = ['dangdang.com','ddimg.cn']
    start_urls = ['http://category.dangdang.com/cp01.00.00.00.00.00.html']

    def start_requests(self):
        yield Request(url=self.start_urls[0], callback=self.parse, encoding='utf-8')

    def parse(self, response):
        categories = response.xpath('//div[@id="navigation"]//li[@dd_name="分类"]//div[@class="clearfix"]/span/a')
        if categories:
            for category in categories:
                first_href = category.xpath('./@href').extract()[0]
                if first_href != "/cp01.74.00.00.00.00.html":
                    first_url = parse.urljoin('http://category.dangdang.com/', first_href)
                    yield Request(url=first_url, callback=self.parse, encoding='utf-8')
        else:
            # self.get_book_infos(response)       # 无效
            book_list = response.css('div#search_nature_rg>ul>li')
            if book_list:
                brandcrumbs = response.xpath('//div[@id="breadcrumb"]/div[@class="crumbs_fb_left"]/div[@class="select_frame"]/a/text()').extract()
                categories = []
                for brandcrumb in brandcrumbs[1:]:
                    categories.append(brandcrumb.strip())
                for i in range(len(book_list)):
                    # bookitem = DdangBooksItem()
                    # id = int(re.search('p(\d+)', book.xpath('./@id').extract()[0]).group(1))
                    item_loader = BookItemLoader(item=DdangBooksItem(), response=response)
                    i = str(i + 1)
                    item_loader.add_css('id', 'div#search_nature_rg>ul>li:nth-child(' + i + ')::attr(id)')
                    item_loader.add_css('name', 'div#search_nature_rg>ul>li:nth-child(' + i + ')>a::attr(title)')
                    img_url = response.css('div#search_nature_rg>ul>li:nth-child(' + i + ')>a>img::attr(data-original)').extract()
                    # img_src = response.css('div#search_nature_rg>ul>li:nth-child('+i+')>a>img::attr(src)').extract()
                    if not img_url:
                        img_url = response.css('div#search_nature_rg>ul>li:nth-child(' + i + ')>a>img::attr(src)').extract()
                    item_loader.add_value('image_url', [img_url])
                    author = response.css('div#search_nature_rg>ul>li:nth-child(' + i + ')>p.search_book_author>span:nth-child(''1)>a::attr(title)').extract()
                    if not author:
                        author = '缺'
                    item_loader.add_value('author', author)
                    pub_time = response.css('div#search_nature_rg>ul>li:nth-child(' + i + ')>p.search_book_author>span:nth-child(''2)::text').extract()
                    if not pub_time:
                        pub_time = '2020-01-01'
                    item_loader.add_value('pub_time', pub_time)
                    publisher = response.css('div#search_nature_rg>ul>li:nth-child(' + i + ')>p.search_book_author>span:nth-child(''3)>a::attr(title)').extract()
                    if not publisher:
                        publisher = "缺"
                    item_loader.add_value('publisher', publisher)
                    item_loader.add_css('price', 'div#search_nature_rg>ul>li:nth-child(' + i + ')>p.price>span.search_now_price::text')
                    item_loader.add_css('title', 'div#search_nature_rg>ul>li:nth-child(' + i + ')>p.name>a::text')
                    item_loader.add_css('comment_nums', 'div#search_nature_rg>ul>li:nth-child(' + i + ')>p.search_star_line>a::text')
                    item_loader.add_css('star_level', 'div#search_nature_rg>ul>li:nth-child(' + i + ')>p.search_star_line>span>span::attr(style)')
                    item_loader.add_value('category_1', categories[0])
                    categories.extend([" "," "])
                    item_loader.add_value('category_2', categories[1])
                    item_loader.add_value('category_3', categories[2])
                    item_loader.add_css('book_url', 'div#search_nature_rg>ul>li:nth-child(' + i + ')>a::attr(href)')
                    item_loader.add_css('image_alt', 'div#search_nature_rg>ul>li:nth-child(' + i + ')>a>img::attr(alt)')

                    bookitem = item_loader.load_item()
                    yield bookitem

                    page_num_str = response.css('div#go_sort div.data>:nth-child(3)::text').extract()[0].strip()
                    page_num = int(re.match('/(\d+)', page_num_str).group(1))
                    if page_num > 1:
                        for i in range(2, page_num + 1):
                            next_page_url = 'http://category.dangdang.com/pg' + str(i) + '-' + response.url[-24:]
                            yield Request(url=next_page_url, callback=self.parse, encoding='utf-8')
                            
