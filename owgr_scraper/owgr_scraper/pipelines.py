# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import psycopg2
from .config import HOSTNAME, USERNAME, PASSWORD, DATABASE
from .items import Player, PlayerResult
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
        self.cur.execute('delete from "PlayerEvents"')

        self.cur.execute('delete from "Players"')

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        if isinstance(item, Player):
            self.cur.execute('insert into "Players"(player_id, player_name) values(%s,%s)',
                             (item['player_id'], item['player_name']))
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
        return item
