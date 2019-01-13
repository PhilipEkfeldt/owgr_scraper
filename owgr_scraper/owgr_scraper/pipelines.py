# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import psycopg2
from .config import HOSTNAME, USERNAME, PASSWORD, DATABASE
from .items import Player, PlayerResult, Tournament, RankingUpdatedDate
from .spiders.player_data import PlayerDataSpider
from .spiders.CurrentTournaments import CurrentTournamentsSpider
# Code taken from https://medium.com/codelog/store-scrapy-crawled-data-in-postgressql-2da9e62ae272 and modified


class PostgresPipeline(object):

    def open_spider(self, spider):
        hostname = HOSTNAME
        username = USERNAME
        password = PASSWORD
        database = DATABASE

        self.connection = psycopg2.connect(
            host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()
        if isinstance(spider, PlayerDataSpider):
            self.cur.execute('delete from "PlayerEvents"')
            self.connection.commit()

            self.cur.execute('delete from "Players"')
            self.connection.commit()

            self.cur.execute('delete from "RankingUpdatedDate"')
            self.connection.commit()

        elif isinstance(spider, CurrentTournamentsSpider):
            self.cur.execute('delete from "CurrentTournaments"')
            self.connection.commit()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        if isinstance(item, Player):
            self.cur.execute('insert into "Players"(player_id, player_name, current_rank) values(%s,%s,%s)',
                             (item['player_id'], item['player_name'], item['rank']))
            self.connection.commit()
        elif isinstance(item, PlayerResult):
            self.cur.execute('insert into "PlayerEvents"( player_id, \
                                                            event_id, \
                                                            event_name, \
                                                            tour, \
                                                            week, \
                                                            year, \
                                                            finish, \
                                                            points, \
                                                            weight, \
                                                            adj_points \
                                                            ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                             (item['player_id'],
                              item['event_id'],
                              item['event_name'],
                              item['tour'],
                              item['week'],
                              item['year'],
                              item['finish'],
                              item['points'],
                              item['weight'],
                              item['adj_points']))
            self.connection.commit()
        elif isinstance(item, Tournament):
            self.cur.execute('insert into "CurrentTournaments"(name, tour, field_strength, points) values(%s,%s, %s, %s)',
                             (item['name'], item['tour'], item['field_strength'], item['points']))
            self.connection.commit()
        elif isinstance(item, RankingUpdatedDate):
            print(item)
            self.cur.execute('insert into "RankingUpdatedDate"(date) values(%s)',
                             (item['date'],))
            self.connection.commit()
        return item
