# Experiments with website scraping 

Collection of Python script to scrape different websites. Currently supported sites are:
* Yahoo Finance: Extract stock and ETF information
* Staking Rewards: Extract coin information with rewards statistics

## Requirements

This scraping scripts require to install: 

* some Python libraries list in the `requirements.txt` file: `pip install -r requirements.txt`
* The Mozilla Firefox browser
* The Mozilla Firefox Gecko driver which can be downloaded here: [https://github.com/mozilla/geckodriver/releases](https://
github.com/mozilla/geckodriver/releases)

## Usage

### Yahoo Finance scraper

TODO

### Stacking Rewards scraper

The Stacking Rewards scaper `sw_scraper.py` module can be executed standalone as follows:

```
python sw_scraper.py --pages 1-10 --format table
```

You can choose which pages to scrape (from 1 to 12) and in which format output the results, either
'table' to print a nicely formatted table on screen or 'csv' to print to a CSV file.

