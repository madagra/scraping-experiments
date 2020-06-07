
import os
import pytest

@pytest.fixture
def fsct_symbol_url():
    return "FSCT", "https://finance.yahoo.com/quote/FSCT"

@pytest.fixture
def fsct_html():
    html_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
        "resources", "fsct_mock.html")
    with open(html_file, "r") as f:
        html = f.read()
    return html
