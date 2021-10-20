import csv
import time
from typing import List
from datetime import date, datetime

from scrapers.sw_scaper import ScraperResult, scrape_reward_data


PAGES = range(1, 11)

COLUMNS = ["Date", "Ticker", "Price", "Market cap (USD)", "Reward (%)", "Staked value (USD)"]


def save_to_csv(results: List[ScraperResult]):

    with open("sw_results.csv", "w", newline="") as csvfile:

        writer = csv.writer(csvfile, delimiter=",", quotechar='|', quoting=csv.QUOTE_MINIMAL)
        now = datetime.now()
        writer.writerow(COLUMNS)
        for r in results:
            row = [now, r.ticker, r.price, r.market_cap_usd, r.reward, r.staked_value_usd]
            writer.writerow(row)

if __name__ == "__main__":
    res = scrape_reward_data(pages=list(PAGES))
    save_to_csv(res)
