from binance.client import Client
from defy.PriceFinder import PriceFinder
from tabulate import tabulate
import os


class BinanceFutures:
    def __init__(self, priceFinder):
        self.platformName = "Binance Futures"

        self.binanceApiKey = os.getenv("binance_api_key")
        self.binanceApiSecret = os.getenv("binance_api_secret")
        self.headers = [self.platformName, "Position", "PNL", "ROE %", "Balance ($)"]

        self.priceFinder = priceFinder
        self.client = Client(self.binanceApiKey, self.binanceApiSecret)

    def isUsable(self):
        return self.binanceApiSecret is not None and self.binanceApiSecret is not None

    def getWallet(self, hideSmallBal=True):
        if not self.isUsable():
            return []

        wallet = []
        usdAccount = self.client.futures_account()
        positions = usdAccount["positions"]

        for rawPos in positions:
            symbol = rawPos["symbol"]
            pnl = float(rawPos["unrealizedProfit"])
            pos = float(rawPos["positionInitialMargin"])

            if pos != 0:
                balInDollar = pos + pnl
                roe = pnl / pos * 100

                if hideSmallBal and balInDollar < 1:
                    continue

                wallet.append(
                    {
                        "symbol": symbol,
                        "pos": pos,
                        "pnl": pnl,
                        "roe": roe,
                        "balInDollar": balInDollar,
                    }
                )

        return wallet

    def walletToTable(self, wallet):
        tabulateWallet = []

        for token in wallet:
            tabulateWallet.append(
                [
                    token["symbol"],
                    token["pos"],
                    token["pnl"],
                    token["roe"],
                    token["balInDollar"],
                ]
            )

        return tabulateWallet

    def displayWallet(self, wallet):
        print(
            tabulate(
                self.walletToTable(wallet),
                self.headers,
                floatfmt=(".f", ".2f", ".4f", ".2f", ".2f"),
                tablefmt="simple",
            ),
            "\n",
        )
