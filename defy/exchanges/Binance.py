from binance.client import Client
from tabulate import tabulate
import os

class Binance:
    def __init__(self, priceFinder):
        self.platformName = "Binance"

        self.binanceApiKey = os.getenv('binance_api_key')
        self.binanceApiSecret = os.getenv('binance_api_secret')
        self.headers = [self.platformName, "Price", "Balance", "Balance ($)"]

        self.priceFinder = priceFinder

    def getWallet(self, hideSmallBal=True):
        wallet = []
        client = Client(self.binanceApiKey, self.binanceApiSecret)
        tokens = client.get_account()["balances"]

        for token in tokens:
            symbol = token["asset"]
            price = self.priceFinder.getTokenPrice(symbol)
            bal = float(token["free"]) + float(token["locked"])
            balInDollar = bal * price

            if bal == 0 or (hideSmallBal and balInDollar < 1):
                continue

            wallet.append([symbol, price, bal, balInDollar])
        
        return wallet
    
    def displayWallet(self, wallet):
        print(tabulate(wallet, self.headers, floatfmt=(".f", ".2f", ".4f", ".2f"), tablefmt="simple"), "\n")