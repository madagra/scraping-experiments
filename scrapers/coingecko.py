from dataclasses import dataclass
from typing import List

from pycoingecko import CoinGeckoAPI

COINS_MAPPING = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    # "BNB",
    # "ADA"
    # "SOL"
    # "LUNA"
    # "DOT"
    # "AVAX"
    # "MATIC"
    # "ALGO"
    # "LINK"
    # "TRN"
    # "XLM"
    # "ATOM"
    # "FTM"
    # "THETA"
    # "EGLD"
    # "CAKE"
    # "ICP"
    # "XTZ"
    # "RUNE"    
}


@dataclass
class CoinGeckoResult:
    ticker: str = ""
    price_usd: float = 0.
    price_eur: float = 0.
    market_cap_usd: float = None
    market_cap_eur: float = None
    market_cap_rank: int = None
    circulating_supply: float = None
    fully_diluted_market_cap_usd: float = None
    fully_diluted_market_cap_eur: float = None
    max_supply: float = None
    total_volume_usd: float = None,
    total_volume_eur: float = None
    ath_usd: float = None
    ath_eur: float = None
    ath_change_percentage: float = None
    ath_date: str = None
    atl_usd: float = None
    atl_eur: float = None
    atl_change_percentage: float = None
    atl_date: str = None
    

def _fetch_market_data_coin(coin: str, cg: CoinGeckoAPI):
    """Extract coin result from CoinGecko API
    
    NOTICE: The number of calls to this function must be limited
    """
    try:    
        coin_data = cg.get_coin_by_id(coin, localization=False)
        market_data = coin_data["market_data"]
    except ValueError:
        print(f"Coin {coin} not found, skipping...")
        return
       
    res = CoinGeckoResult()
    
    res.ticker = coin_data["symbol"].capitalize()
    res.price_usd = market_data["current_price"]["usd"]
    res.price_eur = market_data["current_price"]["eur"]
    res.market_cap_usd = market_data["market_cap"]["usd"]
    res.market_cap_eur = market_data["market_cap"]["eur"]
    res.fully_diluted_market_cap_usd = market_data["fully_diluted_valuation"]["usd"]
    res.fully_diluted_market_cap_eur = market_data["fully_diluted_valuation"]["eur"]
    res.market_cap_rank = market_data["market_cap_rank"]
    res.total_volume_usd = market_data["total_volume"]["usd"]
    res.total_volume_eur = market_data["total_volume"]["eur"]
    res.circulating_supply = market_data["circulating_supply"]
    res.max_supply = market_data["total_supply"]
    res.ath_usd = market_data["ath"]["usd"]
    res.ath_eur = market_data["ath"]["eur"]
    res.ath_change_percentage = market_data["ath_change_percentage"]["usd"]
    res.ath_date = market_data["ath_date"]["usd"]
    res.atl_usd = market_data["atl"]["usd"]
    res.atl_eur = market_data["atl"]["eur"]
    res.atl_change_percentage = market_data["atl_change_percentage"]["usd"]
    res.atl_date = market_data["atl_date"]["usd"]

    return res
    

def fetch_market_data():

    cg = CoinGeckoAPI()

    results = []

    for ticker, coin in COINS_MAPPING.items():

        tmp = _fetch_market_data_coin(coin, cg)
        results.append(tmp)


if __name__ == "__main__":
    fetch_market_data()
    