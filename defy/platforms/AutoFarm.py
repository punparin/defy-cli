from configparser import ConfigParser
from web3 import Web3
from tabulate import tabulate
from defy.Utilities import Utilities
from defy.PriceFinder import PriceFinder
import json
import os
import requests


class AutoFarm:
    def __init__(self, priceFinder):
        self.config = ConfigParser(os.environ)

        self.config.read("./config.ini")

        self.platformName = "autofarm"
        self.contractAddress = "0x0895196562C7868C5Be92459FaE7f877ED450452"
        self.networkProvider = self.config["DEFAULT"]["network_provider"]
        self.autoFarmEndpoint = self.config["DEFAULT"]["autofarm_endpoint"]
        self.headers = [
            self.platformName,
            "Deposit",
            "Reward (AUTO)",
            "Balance ($)",
        ]

        self.web3 = Web3(Web3.HTTPProvider(self.networkProvider))
        self.priceFinder = priceFinder

        with open("abis/autofarm_abi.json", "r") as abi_definition:
            self.autoFarmAbi = json.load(abi_definition)

    def getWallet(self, walletAddress, hideSmallBal=True):
        platformFarms = []
        r = requests.get(self.autoFarmEndpoint)
        farms = r.json()["pools"]

        for farmId in farms:
            farm = farms[farmId]
            deposit = self.getTokenBalance(int(farmId), walletAddress)

            if deposit != 0:
                symbol = farm["wantName"]
                reward = self.getReward(int(farmId), walletAddress)
                price = float(farm["wantPrice"])
                rewardPrice = self.priceFinder.getTokenPrice("AUTO")
                balInDollar = deposit * price + reward * rewardPrice

                if hideSmallBal and balInDollar < 1:
                    continue

                platformFarms.append(
                    {
                        "symbol": symbol,
                        "deposit": deposit,
                        "reward": reward,
                        "balInDollar": balInDollar,
                    }
                )

        return platformFarms

    def getTokenBalance(self, farmId, walletAddress):
        contract = self.web3.eth.contract(
            abi=self.autoFarmAbi, address=Web3.toChecksumAddress(self.contractAddress)
        )
        bal = Utilities.formatBalance(
            self.web3,
            contract.functions.stakedWantTokens(
                farmId, Web3.toChecksumAddress(walletAddress)
            ).call(),
        )

        return bal

    def getReward(self, farmId, walletAddress):
        contract = self.web3.eth.contract(
            abi=self.autoFarmAbi, address=Web3.toChecksumAddress(self.contractAddress)
        )

        reward = Utilities.formatBalance(
            self.web3,
            contract.functions.pendingAUTO(
                farmId, Web3.toChecksumAddress(walletAddress)
            ).call(),
        )

        return reward

    def walletToTable(self, wallet):
        tabulateWallet = []

        for token in wallet:
            tabulateWallet.append(
                [
                    token["symbol"],
                    token["deposit"],
                    token["reward"],
                    token["balInDollar"],
                ]
            )

        return tabulateWallet

    def displayWallet(self, wallet):
        print(
            tabulate(
                self.walletToTable(wallet),
                self.headers,
                floatfmt=(".f", ".4f", ".4f", ".2f", ".2f"),
                tablefmt="simple",
            ),
            "\n",
        )
