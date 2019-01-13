# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PlayerResult(scrapy.Item):
    player_id = scrapy.Field()
    event_id = scrapy.Field()
    event_name = scrapy.Field()
    tour = scrapy.Field()
    week = scrapy.Field()
    year = scrapy.Field()
    finish = scrapy.Field()
    points = scrapy.Field()
    weight = scrapy.Field()
    adj_points = scrapy.Field()


class Player(scrapy.Item):
    player_id = scrapy.Field()
    player_name = scrapy.Field()
    rank = scrapy.Field()


class Tournament(scrapy.Item):
    name = scrapy.Field()
    tour = scrapy.Field()
    field_strength = scrapy.Field()
    points = scrapy.Field()


class RankingUpdatedDate(scrapy.Item):
    date = scrapy.Field()
