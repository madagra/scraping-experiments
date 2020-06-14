import re
from enum import Enum
from dataclasses import dataclass, field
import requests
from bs4 import BeautifulSoup 


@dataclass
class ScraperResult:
    full_name: str = ""
    symbol: str = ""
    close_price: float = 0.
    eps: float = 0.


class YfIndicator(Enum):
    PREV_CLOSE = "PREV_CLOSE-value",
    EPS = "EPS_RATIO-value"
    

def yf_url_generation(symbol: str) -> str:
    # TODO: sanitize input
    base_url = "https://finance.yahoo.com/quote"
    return f"{base_url}/{symbol}"

def yf_url_request(url: str) -> dict:

    res = {
        "result": None,
        "code": 408
    }

    try:
        response = requests.get(url)
        res["code"] = response.status_code
        if len(response.history) != 0 or response.status_code != 200:
            res["code"] = 400
        elif response.status_code == 200:
            res["result"] = response.content
    except requests.HTTPError:
        pass
    return res

def _yf_get_symbol_name(full_str) -> (str, str):
    full_name, symbol = "", ""
    regex = re.compile(r"^(.*)\s\-\s(.*)")
    match = regex.match(full_str)
    if match is not None and len(match.groups()) == 2:
        full_name = match.group(2)
        symbol = match.group(1)
    return full_name, symbol

def _yf_get_trading_value(parsed_html: BeautifulSoup, 
        value_type: YfIndicator) -> float:
    res = None
    try:
        assert isinstance(value_type, YfIndicator)
        tag = parsed_html.find_all("td", attrs={"data-test": value_type.value})
        if len(tag) == 1:
            value = tag[0].span.contents
            res = float(value[0])
    except (AssertionError, AttributeError) :
        pass
    return res

def yf_scraper(html_content: str) -> ScraperResult:

    res = ScraperResult()    
    parsed_html = BeautifulSoup(html_content, "html.parser")

    # extract full name and symbol
    full_name_tag = parsed_html.find_all("h1", attrs={"data-reactid": "7"})
    if len(full_name_tag) == 1:
        tmp = full_name_tag[0].string.extract()
        res.full_name, res.symbol = _yf_get_symbol_name(tmp)

    # extract financial indicators
    res.close_price = _yf_get_trading_value(parsed_html, YfIndicator.PREV_CLOSE)
    res.eps = _yf_get_trading_value(parsed_html, YfIndicator.EPS)
    
    return res

def scrape_symbol_data(symbol: str) -> ScraperResult:
    """
    Scraper driver function which starting from a stock symbol scrapes the
    associated trading data from Yahoo Finance website

    Parameters
    ----------
    symbol: the stock ticker symbol to retrieve

    Returns
    -------
    a ScraperResult instance filled with scraped results
    """
    res = ScraperResult()
    try:
        html_content = yf_url_request(yf_url_generation(symbol))["result"]
        if html_content is not None:
            res = yf_scraper(html_content)
    except KeyError:
        pass
    return res

