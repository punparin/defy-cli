from binance.client import Client
from tabulate import tabulate
import os


class Binance:
    def __init__(self, priceFinder):
        self.platformName = "Binance"

        self.binanceApiKey = os.getenv("binance_api_key")
        self.binanceApiSecret = os.getenv("binance_api_secret")
        self.headers = [self.platformName, "Price", "Balance", "Balance ($)"]

        self.priceFinder = priceFinder
        self.client = Client(self.binanceApiKey, self.binanceApiSecret)

    def isUsable(self):
        return self.binanceApiSecret is not None and self.binanceApiSecret is not None

    def getWallet(self, hideSmallBal=True):
        if not self.isUsable():
            return []

        wallet = []
        tokens = self.client.get_account()["balances"]

        for token in tokens:
            symbol = token["asset"]
            price = self.priceFinder.getTokenPrice(symbol)
            bal = float(token["free"]) + float(token["locked"])
            balInDollar = bal * price

            if bal == 0 or (hideSmallBal and balInDollar < 1):
                continue

            wallet.append(
                {
                    "symbol": symbol,
                    "price": price,
                    "bal": bal,
                    "balInDollar": balInDollar,
                }
            )

        return wallet

    def walletToTable(self, wallet):
        tabulateWallet = []

        for token in wallet:
            tabulateWallet.append(
                [token["symbol"], token["price"], token["bal"], token["balInDollar"]]
            )

        return tabulateWallet

    def displayWallet(self, wallet):
        print(
            tabulate(
                self.walletToTable(wallet),
                self.headers,
                floatfmt=(".f", ".2f", ".4f", ".2f"),
                tablefmt="simple",
            ),
            "\n",
        )
