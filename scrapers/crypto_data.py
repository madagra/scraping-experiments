from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

coin_list = cg.get_coins_list()
coin_data = cg.get_coin_by_id("ethereum", localization=False)

breakpoint()