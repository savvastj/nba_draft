import requests
import pandas as pd
from pyquery import PyQuery as pq

## This module contains some helper functions used to scrape the player stats
## from Draft Ex

# columns used when scraping data for DX's basic player stats
# Note that "box" and "Team_Logo" are jusy placehodlers for columns
# that don't have any info and should be dropped when cleaning up
# the data
basic_stats_cols = ["box", "Player", "Team_Logo", "Team", "G", "MP", "PTS",
                    "FG_2P", "FG_2PA",  "FG_2P_Pct", "FG_3P", "FGA_3P",
                    "FG_3P_Pct", "FT", "FTA", "FT_Pct", "OREB", "DREB", "REB",
                    "AST", "STL", "BLK", "TO", "PF"]

# columns used when scraping DX's player usage data
# Again note that box and Team_logo columns are useless
usage_cols = ["box", "Player", "Team_Logo", "Team", "G", "MP", "PER", "EFF",
              "EFF_per_40",  "EWA", "Poss_per_G", "Tm_Poss_per_G",
              "Pct_of_Tm_Poss", "Pts_per_Poss", "FGA_per_Poss", "FTA_per_Poss",
              "AST_per_Poss", "TO_per_Poss"]

# efficiency columns
eff_cols = ["box", "Player", "Team_Logo", "Team", "G", "MP", "PTS", "FGA",
            "PTS_per_Play", "TS_Pct", "eFG_Pct", "FT_Rate", "Three_Pt_Rate",
            "AST", "AST_to_FGA_Ratio", "AST_to_TO_Ratio", "PPR", "STL", "BLK",
            "PF"]

def create_pq(url):
    """Creates PyQuery object used for scraping"""
    response = requests.get(url)
    html = response.text
    return pq(html)

def get_last_pg(url):
    """Get the last page number to be scraped"""
    pq_obj = create_pq(url)
    last_pg_selector = ".disabled+ li a"
    last_pg = pq_obj(last_pg_selector)
    return last_pg[0].text_content()

def get_links(pq_obj, url_selector):
    """Gets the links associated with the given css selector"""
    urls = pq_obj(url_selector)
    links = [url.get("href") for url in urls]
    return links

def get_data(pq_obj, row_selector):
    """Get table data"""
    rows = pq_obj(row_selector)
    data = [[td.text_content() for td in row] for row in rows]
    return data

def create_df(url, cols):
    """Scrapes data from url and returns a DataFrame with given columns"""
    pq_obj = create_pq(url)

    # Extract the links for the players and teams
    player_selector = "#cmn_wrap > div.row.two-cols > div >"\
                      "div.row.inner-page.stats > div > table > tbody > tr > "\
                      "td.text.key > a"
    player_links = get_links(pq_obj, player_selector)
    team_selector = ".key~ .text+ td a"
    team_links = get_links(pq_obj, team_selector)

    # get the table data
    row_selector = "#cmn_wrap > div.row.two-cols > div > "\
                   "div.row.inner-page.stats > div > table > tbody > tr"
    data = get_data(pq_obj, row_selector)

    df = pd.DataFrame(data=data, columns=cols)
    df["Player_Link"] = player_links
    df["Team_Link"] = team_links

    return df
