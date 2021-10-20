import pytest
import scrapers.yf_scraper as scraper
from scrapers.yf_scraper import ScraperResult, YfIndicator


def test_url_generation(fsct_symbol_url):
    
    symbol = fsct_symbol_url[0]
    expected_url = fsct_symbol_url[1]

    actual_url = scraper.yf_url_generation(symbol)
    assert actual_url == expected_url

def test_url_request(fsct_symbol_url):
    
    url = fsct_symbol_url[1]
    actual_resp = scraper.yf_url_request(url)

    assert type(actual_resp) == dict
    assert "result" in actual_resp 
    assert "code" in actual_resp
    assert actual_resp["code"] == 200

@pytest.mark.parametrize("malformed_url", 
    [   
        "https://finance.yahoo.com/quote/AAAA",
        "https://finance.yahoo.com/quote/^$*@%&#*$#@*",
        "https://finance.yahoo.com/quote/$#&@@@!%&%#"
    ]
)
def test_malformed_url_request(malformed_url):

    actual_resp = scraper.yf_url_request(malformed_url)

    assert type(actual_resp) == dict
    assert "result" in actual_resp 
    assert "code" in actual_resp
    assert actual_resp["code"] == 400
    assert actual_resp["result"] is None

@pytest.mark.parametrize("full_name_str", ["FSCT - Forescout Technologies, Inc."])
def test_get_symbol_name(full_name_str):
    expected_resp = "Forescout Technologies, Inc.", "FSCT"
    actual_resp = scraper._yf_get_symbol_name(full_name_str)
    assert actual_resp == expected_resp

def test_get_trading_value_prevclose(parsed_fsct_html):
    expected_value = 23.1
    value = scraper._yf_get_trading_value(parsed_fsct_html, YfIndicator.PREV_CLOSE)
    assert type(value) == float
    assert value == expected_value

def test_get_trading_value_eps(parsed_fsct_html):
    expected_value = -3.09
    value = scraper._yf_get_trading_value(parsed_fsct_html, YfIndicator.EPS)
    assert type(value) == float
    assert value == expected_value

def test_get_trading_value_wrong(parsed_fsct_html):
    value = scraper._yf_get_trading_value(parsed_fsct_html, "")
    assert value is None

def test_yf_scraper_stock(fsct_html):
    
    expected_res = ScraperResult(
        full_name="Forescout Technologies, Inc.",
        symbol="FSCT",
        open_price=23.10,
        close_price=23.1,
        ask=22.85,
        bid=21.80,
        eps=-3.09
    )

    actual_res = scraper.yf_scraper(fsct_html)

    assert isinstance(actual_res, ScraperResult)
    assert expected_res == actual_res

def test_yf_scraper_etf(ievl_html):
    
    expected_res = ScraperResult(
        full_name="iShares Edge MSCI Europe Value Factor UCITS ETF EUR (Acc)",
        symbol="IEVL.L",
        open_price=5.34,
        close_price=5.31,
        ask=5.27,
        bid=5.27
    )

    actual_res = scraper.yf_scraper(ievl_html)

    assert isinstance(actual_res, ScraperResult)
    assert expected_res == actual_res


@pytest.mark.parametrize("symbol", [ "FSCT", "AMD", "MSFT", "AAPL"]) 
def test_scrape_symbol_stocks(symbol):
    res = scraper.scrape_symbol_data(symbol)
    assert isinstance(res, ScraperResult)
    assert res.full_name and res.symbol
    assert res.symbol == symbol
    assert res.open_price > 0
    assert res.close_price > 0
    assert res.ask > 0
    assert res.bid > 0
    assert res.eps**2 > 0


@pytest.mark.parametrize("symbol", ["CMUD.PA", "IEVL.L"]) 
def test_scrape_symbol_etfs(symbol):
    res = scraper.scrape_symbol_data(symbol)
    assert isinstance(res, ScraperResult)
    assert res.full_name and res.symbol
    assert res.symbol == symbol
    assert res.open_price > 0
    assert res.close_price > 0
    assert res.ask is None or res.ask > 0 
    assert res.bid is None or res.bid > 0 
    assert res.eps is None