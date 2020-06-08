
import os
import pytest
from bs4 import BeautifulSoup

fsct_html_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources", "FSCT.html")

@pytest.fixture
def fsct_symbol_url():
    return "FSCT", "https://finance.yahoo.com/quote/FSCT"

@pytest.fixture
def fsct_html():
    with open(fsct_html_file, "r") as f:
        html_content = f.read()
    return html_content

@pytest.fixture
def parsed_fsct_html():
    with open(fsct_html_file, "r") as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, "html.parser")
    return soup
