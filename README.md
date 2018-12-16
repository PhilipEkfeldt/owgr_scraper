# OWGR (Official World Golf Ranking) Forecaster
## THIS IS A WORK IN PROGRESS

### Currently implemented:
 - Scrapy implementation for scraping the Official World Golf Ranking site, including:
   -  Player result in OWGR sanctioned events within in the last 104 weeks (rolling period for ranking calculation).
   -  X first players on ranking (scraped at the same time as results).
   -  Current week's events.
 -  Data is stored in postgressql database through pipeline. Update the config.py file with correct database information for it to work. See Scrapy docs for how to run crawlers/spiders.
### Planned:
 - Scrape/fetch leaderboard information for the largest tours (PGA Tour, European Tour to start with).
 - Make exact forecast of ranking based on current standings in ongoing tournaments.
 - Create webapp to display forecasted rankings.
   - Including making own scenarios for where players place in their current tournament (if playing)
