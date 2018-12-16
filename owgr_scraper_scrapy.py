import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from scrapy.crawler import CrawlerProcess

import pandas as pd
import util
from bs4 import BeautifulSoup

# ['player_id', 'player_name', 'event_id', 'event_name',
#                                 'tour', 'week', 'year', 'finish', 'points', 'weight', 'adj_points'])


class PlayerDataSpider(scrapy.Spider):
    nr_players = 1

    def __init__(self, nr_players="1", *args, **kwargs):
        super(PlayerDataSpider, self).__init__(*args, **kwargs)
        self.nr_players = int(nr_players)

    name = 'PlayerData'
    start_urls = ["http://www.owgr.com/ranking?pageNo=1&pageSize=%d&country=All" % (
        nr_players)]
    urls = []

    def parse_player_page(self, response):
        rows = response.xpath(
            '//*[@id="player_results"]/*[@class="table_container"]/table//tr')[1:]
        items = []
        for row in rows:
            item = PlayerResult()
            item['event_id'] = row.xpath('.//a/@href').extract()
            items.append(item)
        return items

    def parse(self, response):
        urls = response.xpath(
            '//*[@id="ranking_table"]/*[@class="table_container"]/table//a/@href').extract()
        items = []
        for url in urls:
            new_items = yield response.follow(url, self.parse_player_page)
            items.append(new_items)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(PlayerDataSpider)
process.start()  # the script will block here until the crawling is finished


def scrape_player_data(nr_players):
    url = "http://www.owgr.com/ranking?pageNo=1&pageSize=%d&country=All" % (
        nr_players)
    r = requests.get(url)
    html = r.text

    soup = BeautifulSoup(html, features='lxml')
    form = soup.body.form
    maindiv = form.find(lambda tag: tag.has_attr(
        'id') and tag['id'] == "site_container")
    main_content_div = maindiv.find(
        lambda tag: tag.has_attr('id') and tag['id'] == "main_content")

    ranking_table = main_content_div.find(
        lambda tag: tag.has_attr('id') and tag['id'] == "ranking_table")

    table_container = ranking_table.find(lambda tag: tag.has_attr(
        'class') and tag['class'] == ['table_container'])
    table = table_container.table

    linktags = table.find_all(
        lambda tag: tag.has_attr('href') and tag.name == "a")

    links = list(
        map(lambda tag: "http://www.owgr.com" + tag['href'], linktags))

    data = pd.DataFrame(columns=['player_id', 'player_name', 'event_id', 'event_name',
                                 'tour', 'week', 'year', 'finish', 'points', 'weight', 'adj_points'])
    i = 0
    nr_players = len(links)
    for link in links:
        # Scrape result data from each player's page
        i += 1
        player_id = link.partition("=")[2]
        r = requests.get(link)
        html = r.text
        soup = BeautifulSoup(html, features='lxml')

        form = soup.body.form
        maindiv = form.find(lambda tag: tag.has_attr(
            'id') and tag['id'] == "site_container")
        main_content_div = maindiv.find(
            lambda tag: tag.has_attr('id') and tag['id'] == "main_content")
        player_results_tag = main_content_div.find(
            lambda tag: tag.has_attr('id') and tag['id'] == "player_results")
        table_container = player_results_tag.find(lambda tag: tag.has_attr(
            'class') and tag['class'] == ['table_container'])
        table = table_container.table
        tablerows = table(lambda tag: tag.name == "tr")[1:]

        player_name = str(player_results_tag.h2.string)

        for row in tablerows:
            rowcells = row.find_all(lambda tag: tag.name == "td")
            event_id = rowcells[0].a['href'].partition("=")[2]
            event_name = str(rowcells[0].string)
            tour = str(rowcells[1].string)
            week = int(rowcells[2].string)
            year = int(rowcells[3].string)
            finish = str(rowcells[4].string)
            points = float(rowcells[5].string.replace("-", "0"))
            weight = float(rowcells[6].string)
            adj_points = float(rowcells[7].string.replace("-", "0"))
            data = data.append({"player_id": player_id,
                                "player_name": player_name,
                                "event_id": event_id,
                                "event_name": event_name,
                                "tour": tour,
                                "week": week,
                                "year": year,
                                "finish": finish,
                                "points": points,
                                "weight": weight,
                                "adj_points": adj_points}, ignore_index=True)
        # Progress
        util.progress(i, nr_players, "players scraped")
    return data


def scrape_current_tournament_data():
    url = "http://www.owgr.com/events"
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, features='lxml')

    events = pd.DataFrame(columns=['name', 'tour', 'field_strength', 'points'])
    table = soup.find(lambda tag: tag.has_attr(
        'id') and tag['id'] == "current_events")
    rows = table.find_all(lambda tag: tag.name == 'tr')
    for row in rows[1:]:
        print(row)
        cells = row.find_all(lambda tag: tag.name == 'td')
        print(cells)
        name = str(cells[0].string)
        tour = str(cells[1].string)
        field_strength = int(cells[2].string.replace('-', '0'))
        points = int(cells[3].string)
        events = events.append({'name': name,
                                'tour': tour,
                                'field_strength': field_strength,
                                'points': points},
                               ignore_index=True)
    return events


def get_current_pgatour_tournament_ids():
    r = requests.get("https://statdata.pgatour.com/r/current/message.json")
    tournament_id = r.json()['tid']


# get_current_pgatour_tournament_ids()
