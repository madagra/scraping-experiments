import re
import os
from enum import Enum
import time
from dataclasses import dataclass
from typing import Tuple, Optional, List
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import logging


logger = logging.getLogger(__name__)


os.environ['MOZ_HEADLESS'] = '1'
browser = webdriver.Firefox()

@dataclass
class ScraperResult:
    ticker: str = ""
    price: float = 0.
    market_cap_usd: float = None
    staked_value_usd: float = None
    reward: float = None
    total_staked_pc: float = None
    

def sw_url_generation(page: int = 1, debug: bool = True) -> str:
    if not debug:
        base_url = "https://www.stakingrewards.com/cryptoassets/"
        url = base_url + f"?page={page}&sort=rank_ASC"
        browser.get(url)
        time.sleep(5)
        return browser.page_source
    else:
        with open("example.html", "r") as f:
            html_content = f.read()
        return html_content

def sw_scraper(html_content: str) -> List[ScraperResult]:

    res = []
    parsed_html = BeautifulSoup(html_content, "html.parser")
    table_data = parsed_html.find_all("div", {"class": "rt-tr-group"})

    for row in table_data:
        
        tmp_res = ScraperResult()

        # find the name of the coin
        data = row.find_all("b", {"class": re.compile("brandGroup_name_*")})
        if len(data) != 1:
            logger.warning("Something has changes in the web page and scraping might not work!")
        tmp_res.ticker = data[0].span.contents[0]

        # find the price
        data = row.find_all("span", {"class": "price"})
        if len(data) != 1:
            logger.warning("Something has changes in the web page and scraping might not work!")
        tmp_res.price = float(data[0].contents[0][1:].replace(",", ""))

        # find the reward
        data = row.find_all("div", {"class": "rt-td"})
        for inner_data in data:
            
            a = inner_data.find_all("a", {"href": "/savings/cardano/"})
            if len(a) == 1:
                a_str = a[0].div.contents[0]
                tmp_res.staked_value_usd = float(a_str[1:].replace(",",""))
            
            tmp = inner_data.find_all("a")
            for a in tmp:
                a_str = str(a.contents[0])

                # total staked
                if a_str.endswith("%") and tmp_res.reward is None:
                    tmp_res.reward = float(a_str[:-1])

                # market cap
                if a_str.startswith("$") and tmp_res.market_cap_usd is None:
                    tmp_res.market_cap_usd = float(a_str[1:].replace(",",""))

                # total staked
                if a_str.endswith("%") and tmp_res.total_staked_pc is None:
                    pc_stacked = float(a_str[:-1])
                    tmp_res.total_staked_pc = pc_stacked
        
        res.append(tmp_res)
    
    return res
                

def scrape_reward_data(pages: Optional[List[int]] = None) -> List[ScraperResult]:
    
    res: List[ScraperResult] = []
    if pages is None:
        pages = range(10000)
    
    for page in pages:
        print(f"Scraping page {page}")
        try:
            html_content = sw_url_generation(page, debug=False)
            if html_content is not None:
                tmp = sw_scraper(html_content)
                res.extend(tmp)
        except KeyError as e:
            print(f"Error reading page {page}. Details: {str(e)}")
            break

    return res


if __name__ == "__main__":
    res = scrape_reward_data(pages=[1])
    
    r: ScraperResult
    for r in res:
        print()
        print(f"Currency: {r.ticker}")
        print(f"Market cap: {r.market_cap_usd}")
        print(f"Staking reward: {r.reward}")
        print(f"Total staked: {r.staked_value_usd}")
        print(f"Current price: {r.price}")
        print("-----------")
        time.sleep(1)
