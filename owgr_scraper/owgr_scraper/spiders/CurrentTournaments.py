# -*- coding: utf-8 -*-
import scrapy
from ..items import Tournament


class CurrentTournamentsSpider(scrapy.Spider):
    name = 'CurrentTournaments'
    start_urls = ['http://www.owgr.com/events/']

    def parse(self, response):
        rows = response.xpath('//*[@id="current_events"]//tr')[1:]
        for row in rows:
            item = Tournament()
            item['name'] = row.xpath('.//td/a/text()').extract_first()
            item['tour'] = row.xpath('.//td[2]/text()').extract_first()
            item['field_strength'] = row.xpath(
                './/td[3]/text()').extract_first().replace("-", "0")
            item['points'] = row.xpath(
                './/td[4]/text()').extract_first().replace("-", "0")
            print(item)
            yield item
