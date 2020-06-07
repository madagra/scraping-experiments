import re
from dataclasses import dataclass, field
import requests
from bs4 import BeautifulSoup 


@dataclass
class ScraperResult:
    full_name: str = ""
    symbol: str = ""
    close_price: float = 0.
    eps: float = 0.
    

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

def _yf_get_symbol_name(full_str):
    full_name, symbol = "", ""
    regex = re.compile(r"^(.*)\s*\((.*)\)$")
    match = regex.match(full_str)
    if match is not None and len(match.groups()) == 2:
        full_name = match.group(1).strip()
        symbol = match.group(2)
    return full_name, symbol

def yf_scraper(html_content: str) -> ScraperResult:

    res = ScraperResult()    
    soup = BeautifulSoup(html_content, "html.parser")

    # extract full name
    full_name_tag = soup.find_all("h1", attrs={"data-reactid": "7"})
    if len(full_name_tag) == 1:
        tmp = full_name_tag[0].string.extract()
        print(tmp)
        res.full_name, res.symbol = _yf_get_symbol_name(tmp)
      
    return res

