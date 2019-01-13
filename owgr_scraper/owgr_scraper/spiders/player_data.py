# -*- coding: utf-8 -*-
import scrapy
from ..items import PlayerResult, Player, RankingUpdatedDate
from datetime import datetime
import re


class PlayerDataSpider(scrapy.Spider):

    def __init__(self, nr_players="1", *args, **kwargs):
        super(PlayerDataSpider, self).__init__(*args, **kwargs)
        self.start_urls = ["http://www.owgr.com/ranking?pageNo=1&pageSize=%s&country=All" % (
            nr_players)]

    name = 'PlayerData'

    urls = []

    def parse_player_page(self, response):
        rows = response.xpath(
            '//*[@id="player_results"]/*[@class="table_container"]/table//tr')[1:]
        player_id = response.request.url.partition("=")[2]
        player_name = response.xpath(
            '//*[@id="player_results"]/h2/text()').extract_first()
        rank = response.xpath(
            '//*[@id="player_results"]/span[@class="sub_header"]/text()').extract_first().split(' ')[-1]
        yield Player(player_name=player_name,
                     player_id=player_id,
                     rank=rank)

        for row in rows:
            item = PlayerResult()
            item['event_id'] = row.xpath(
                './/a/@href').extract_first().partition("=")[2]
            item['player_id'] = player_id
            item['event_name'] = row.xpath('.//td/a/text()').extract_first()
            item['tour'] = row.xpath('.//td/text()').extract_first()
            item['week'] = row.xpath('.//td[3]/text()').extract_first()
            item['year'] = row.xpath('.//td[4]/text()').extract_first()
            item['finish'] = row.xpath('.//td[5]/text()').extract_first()
            item['points'] = row.xpath(
                './/td[6]/text()').extract_first().replace("-", "0")
            item['weight'] = row.xpath('.//td[7]/text()').extract_first()
            item['adj_points'] = row.xpath(
                './/td[8]/text()').extract_first().replace("-", "0")

            yield item

    def parse(self, response):
        # date parsing solution: https://stackoverflow.com/a/21496318
        def solve(s):
            return re.sub(r'(\d)(st|nd|rd|th)', r'\1', s)
        date = response.xpath(
            '//time[@class="sub_header"]/text()').extract_first()
        date = solve(date)

        date = datetime.strptime(date, "%d %B %Y").date()

        yield RankingUpdatedDate(date=str(date))
        urls = response.xpath(
            '//*[@id="ranking_table"]/*[@class="table_container"]/table//a/@href').extract()
        for url in urls:
            yield response.follow(url, self.parse_player_page)
