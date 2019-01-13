# OWGR (Official World Golf Ranking) Scraper

## Currently implemented:
 - Scrapy implementation for scraping the Official World Golf Ranking site, including:
   -  Player result in OWGR sanctioned events within in the last 104 weeks (rolling period for ranking calculation).
   -  X first players on ranking (scraped at the same time as results).
   -  Current week's events.
 -  Data is stored in postgressql database through pipeline. Update the config.py file with correct database information for it to work. See Scrapy docs for how to run crawlers/spiders.

