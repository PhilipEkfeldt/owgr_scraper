# -*- coding: utf-8 -*-
import scrapy
from ..items import PlayerResult, Player


class PlayerDataSpider(scrapy.Spider):
    name = 'player_data'

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

        yield Player(player_name=player_name,
                     player_id=player_id)

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

            #year = int(rowcells[3].string)
            #finish = str(rowcells[4].string)
            #points = float(rowcells[5].string.replace("-", "0"))
            #weight = float(rowcells[6].string)
            #adj_points = float(rowcells[7].string.replace("-", "0"))
            yield item

    def parse(self, response):
        urls = response.xpath(
            '//*[@id="ranking_table"]/*[@class="table_container"]/table//a/@href').extract()
        for url in urls:
            yield response.follow(url, self.parse_player_page)
