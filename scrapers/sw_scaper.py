import re
import os
import time
from dataclasses import dataclass
from typing import Tuple, Optional, List
from bs4 import BeautifulSoup
from selenium import webdriver
import logging


logger = logging.getLogger(__name__)

MAX_PAGES = 12

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
    price_change_24h: str = None
    

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
        for i, inner_data in enumerate(data):
            
            # first two rows do not contain any interesting data
            if i < 2:
                continue

            try:            

                a_stacked_value = inner_data.find_all("a", {"href": re.compile("savings*")})
                if len(a_stacked_value) > 0:
                    a_str = a_stacked_value[0].div.contents[0]
                    if a_str.startswith("$") and tmp_res.staked_value_usd is None:
                        tmp_res.staked_value_usd = float(a_str[1:].replace(",",""))

                a = inner_data.find_all("a", {"href": re.compile("earn*")})
                if len(a) == 1:
                
                    # price change 24 hours
                    tmp = inner_data.find_all("span", {"class": "row-24-price-change"})
                    if len(tmp) == 1:
                        change = tmp[0].contents[0]
                        tmp_res.price_change_24h = float(change[:-1])

                    tmp = inner_data.find_all("a")
                    for a in tmp:
                        a_str = str(a.contents[0])

                        # market cap
                        if a_str.startswith("$") and tmp_res.market_cap_usd is None:
                            tmp_res.market_cap_usd = float(a_str[1:].replace(",",""))

                        # reward
                        elif a_str.endswith("%") and tmp_res.reward is None:
                            tmp_res.reward = float(a_str[:-1])

                        # total staked percentage
                        elif a_str.endswith("$") and tmp_res.staked_value_usd is None:
                            total_staked_usd = float(a_str[:-1])
                            tmp_res.staked_value_usd = total_staked_usd

                        # total staked percentage
                        elif a_str.endswith("%") and tmp_res.total_staked_pc is None:
                            pc_stacked = float(a_str[:-1])
                            tmp_res.total_staked_pc = pc_stacked

            except ValueError:
                logger.warning("Error reading data row, skipping...")
                break

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


def run_as_script():

    import argparse
    from datetime import datetime, date
    import csv
    import operator

    from tabulate import tabulate

    COLUMNS = ["Date", "Ticker", "Price", "Market cap (USD)", "Reward (%)", "Staked value (USD)"]

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-p",
        "--pages",
        help="The pages of SW data to scrape. Give start and end page separated by dash or 'all' to scrape all the pages. Example: --pages 1-11",
        dest="pages",
        default="1-10",
        required=False,
        type=str,
    )

    parser.add_argument(
        "-f",
        "--format",
        help="The output format. Choose between 'csv' or 'table'. Default is 'table'",
        dest="format",
        default="table",
        required=False,
        type=str
    )

    args = parser.parse_args()

    pages = args.pages.split("-")

    if args.pages == "all":
        pages = (1, MAX_PAGES)

    if len(pages) == 1:
        pages = (int(pages[0]), int(pages[0]))

    pages = tuple([int(p) for p in pages])

    assert pages[0] < pages[1] or pages[0] == pages[1], "Wrong page interval selected"
    if pages[0] > MAX_PAGES or pages[1] > MAX_PAGES:
        raise ValueError(f"You are requesting pages which do not exist! Available pages are from 1 to {MAX_PAGES}")

    pages = range(int(pages[0]), int(pages[1]) + 1)

    results = scrape_reward_data(pages=pages)
    # for r in results:
    #     if r.market_cap_usd is None:
    #         r.market_cap_usd = 0.
    results.sort(key=operator.attrgetter("market_cap_usd"), reverse=True)

    if args.format == "csv":

        with open("sw_results.csv", "w", newline="") as csvfile:

            writer = csv.writer(csvfile, delimiter=",", quotechar='|', quoting=csv.QUOTE_MINIMAL)
            now = datetime.now()
            writer.writerow(COLUMNS)
            for r in results:
                row = [now, r.ticker, r.price, r.market_cap_usd, r.reward, r.staked_value_usd]
                writer.writerow(row)        
    
    elif args.format == "table":
        
        table = {
            "Date": [str(date.today())] * len(results),
            "Ticker": [r.ticker for r in results],
            "Price": [r.ticker for r in results],
            "Market cap (USD)": [r.market_cap_usd for r in results],
            "Reward (%)": [r.reward for r in results],
            "Stacked value (USD)": [r.staked_value_usd for r in results],
            "Stacked percentage (%)": [r.total_staked_pc for r in results],
        }
        print(tabulate(table, headers="keys"))

    else:
        raise NotImplementedError("Use either 'csv' or 'table' as output formats")


if __name__ == "__main__":
    run_as_script()
