from bs4 import BeautifulSoup
import requests
import pandas as pd
import util







# Find links to X first players pages
def scrape_player_data(nr_players):
    url = "http://www.owgr.com/ranking?pageNo=1&pageSize=%d&country=All" % (nr_players)
    r = requests.get(url)
    html = r.text

    soup = BeautifulSoup(html, features = 'lxml')
    form = soup.body.form
    maindiv = form.find(lambda tag : tag.has_attr('id') and tag['id'] == "site_container")
    main_content_div = maindiv.find(lambda tag : tag.has_attr('id') and tag['id'] == "main_content")

    ranking_table = main_content_div.find(lambda tag : tag.has_attr('id') and tag['id'] == "ranking_table")

    table_container = ranking_table.find(lambda tag : tag.has_attr('class') and tag['class'] == ['table_container'] )
    table = table_container.table

    linktags = table.find_all(lambda tag : tag.has_attr('href') and tag.name == "a" )

    links =  list(map(lambda tag : "http://www.owgr.com"  + tag['href'], linktags))

    data = pd.DataFrame(columns=['player_id', 'player_name', 'event_id', 'event_name', 'tour', 'week', 'year', 'finish', 'points', 'weight', 'adj_points'])
    i = 0
    nr_players = len(links)
    for link in links:
        #Scrape result data from each player's page
        i += 1
        player_id = link.partition("=")[2]
        r = requests.get(link)
        html = r.text
        soup = BeautifulSoup(html, features = 'lxml')

        form = soup.body.form
        maindiv = form.find(lambda tag : tag.has_attr('id') and tag['id'] == "site_container")
        main_content_div = maindiv.find(lambda tag : tag.has_attr('id') and tag['id'] == "main_content")
        player_results_tag = main_content_div.find(lambda tag : tag.has_attr('id') and tag['id'] == "player_results")
        table_container = player_results_tag.find(lambda tag : tag.has_attr('class') and tag['class'] == ['table_container'] )
        table = table_container.table
        tablerows = table(lambda tag : tag.name == "tr")[1:]

        player_name = str(player_results_tag.h2.string)

        for row in tablerows:
            rowcells = row.find_all(lambda tag : tag.name == "td")
            event_id= rowcells[0].a['href'].partition("=")[2]
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
        #Progress
        util.progress(i, nr_players, "players scraped")
    return data

player_data = scrape_player_data(100)
player_data.to_csv('scraped.csv', index=False)
