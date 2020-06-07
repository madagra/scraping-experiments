import pytest
import yf_scraper.scraper as scraper
from yf_scraper.scraper import ScraperResult


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

@pytest.mark.parametrize("full_name_str", ["Forescout Technologies, Inc. (FSCT)"])
def test_parse_symbol_fullname(full_name_str):
    
    expected_resp = "Forescout Technologies, Inc.", "FSCT"
    actual_resp = scraper._yf_get_symbol_name(full_name_str)
    assert actual_resp == expected_resp

def test_parse_close_eps(fsct_html):
    pass

def test_scraper(fsct_html):
    
    expected_res = ScraperResult(
        full_name="Forescout Technologies, Inc.",
        symbol="FSCT",
        close_price=24.27,
        eps=-3.09
    )

    actual_res = scraper.yf_scraper(fsct_html)

    assert isinstance(actual_res, ScraperResult)
    assert expected_res == actual_res
