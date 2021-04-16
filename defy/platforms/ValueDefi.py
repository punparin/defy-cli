from configparser import ConfigParser
from web3 import Web3
from tabulate import tabulate
from defy.Utilities import Utilities
from defy.PriceFinder import PriceFinder
import json
import os
import requests


class ValueDefi:
    def __init__(self, priceFinder):
        self.config = ConfigParser(os.environ)

        self.config.read("./config.ini")

        self.platformName = "ValueDefi"
        self.networkProvider = self.config["DEFAULT"]["network_provider"]
        self.valuedefiEndpoint = self.config["DEFAULT"]["valuedefi_endpoint"]
        self.headers = [
            self.platformName,
            "Deposit",
            "Reward",
            "Balance",
            "Balance ($)",
        ]

        self.web3 = Web3(Web3.HTTPProvider(self.networkProvider))
        self.priceFinder = priceFinder

        with open("abis/valuedefi_abi.json", "r") as abi_definition:
            self.valueDefiAbi = json.load(abi_definition)

    def getWallet(self, walletAddress, hideSmallBal=True):
        platformFarms = []
        r = requests.get(self.valuedefiEndpoint)
        farms = r.json()["data"]

        for farm in farms:
            farmingContractAddress = farm["farmingContractAddress"]
            deposit = self.getTokenBalance(farmingContractAddress, walletAddress)

            if deposit != 0:
                pricePerShare = self.getTokenPricePerShare(farmingContractAddress)
                pairSymbol = farm["wantTokenSymbol"]
                mainTokenSymbol, pairTokenSymbol = (
                    pairSymbol.split("-")[0],
                    pairSymbol.split("-")[1],
                )
                mainTokenPrice = self.priceFinder.getTokenPrice(mainTokenSymbol)
                pairTokenPrice = self.priceFinder.getTokenPrice(pairTokenSymbol)
                reward = deposit * pricePerShare - deposit
                bal = deposit + reward
                balInDollar = bal * mainTokenPrice + bal * pairTokenPrice

                if hideSmallBal and balInDollar < 1:
                    continue

                platformFarms.append(
                    {
                        "pairSymbol": pairSymbol,
                        "deposit": deposit,
                        "reward": reward,
                        "bal": bal,
                        "balInDollar": balInDollar,
                    }
                )

        return platformFarms

    def getTokenBalance(self, contractAddress, walletAddress):
        contract = self.web3.eth.contract(
            abi=self.valueDefiAbi, address=Web3.toChecksumAddress(contractAddress)
        )
        bal = Utilities.formatBalance(
            self.web3,
            contract.functions.balanceOf(Web3.toChecksumAddress(walletAddress)).call(),
        )

        return bal

    def getTokenPricePerShare(self, contractAddress):
        contract = self.web3.eth.contract(
            abi=self.valueDefiAbi, address=Web3.toChecksumAddress(contractAddress)
        )
        pricePerShare = Utilities.formatBalance(
            self.web3, contract.functions.getPricePerFullShare().call()
        )

        return pricePerShare

    def walletToTable(self, wallet):
        tabulateWallet = []

        for token in wallet:
            tabulateWallet.append(
                [
                    token["pairSymbol"],
                    token["deposit"],
                    token["reward"],
                    token["bal"],
                    token["balInDollar"],
                ]
            )

        return tabulateWallet

    def displayWallet(self, farms):
        print(
            tabulate(
                self.walletToTable(farms),
                self.headers,
                floatfmt=(".f", ".4f", ".4f", ".2f", ".2f"),
                tablefmt="simple",
            ),
            "\n",
        )
