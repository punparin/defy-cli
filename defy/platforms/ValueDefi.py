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
        self.headers = [self.platformName, "Balance", "Reward", "Balance ($)"]

        self.web3 = Web3(Web3.HTTPProvider(self.networkProvider))
        self.priceFinder = priceFinder

        with open("abis/valuedefi_abi.json", "r") as abi_definition:
            self.abi = json.load(abi_definition)

    def getWallet(self, walletAddress, hideSmallBal=True):
        platformFarms = []
        r = requests.get(self.valuedefiEndpoint)
        farms = r.json()["data"]

        for farm in farms:
            farmingContractAddress = farm["farmingContractAddress"]
            bal = self.getTokenBalance(farmingContractAddress, walletAddress)

            if bal != 0:
                pricePerShare = self.getTokenPricePerShare(farmingContractAddress)
                pairSymbol = farm["wantTokenSymbol"]
                mainTokenSymbol, pairTokenSymbol = (
                    pairSymbol.split("-")[0],
                    pairSymbol.split("-")[1],
                )
                mainTokenPrice = self.priceFinder.getTokenPrice(mainTokenSymbol)
                pairTokenPrice = self.priceFinder.getTokenPrice(pairTokenSymbol)
                reward = bal * pricePerShare - bal
                balInDollar = (bal + reward) * mainTokenPrice + (
                    bal + reward
                ) * pairTokenPrice

                if hideSmallBal and balInDollar < 1:
                    continue

                platformFarms.append([pairSymbol, bal, reward, balInDollar])

        return platformFarms

    def getTokenBalance(self, contractAddress, walletAddress):
        contract = self.web3.eth.contract(
            abi=self.abi, address=Web3.toChecksumAddress(contractAddress)
        )
        bal = Utilities.formatBalance(
            self.web3,
            contract.functions.balanceOf(Web3.toChecksumAddress(walletAddress)).call(),
        )

        return bal

    def getTokenPricePerShare(self, contractAddress):
        contract = self.web3.eth.contract(
            abi=self.abi, address=Web3.toChecksumAddress(contractAddress)
        )
        pricePerShare = Utilities.formatBalance(
            self.web3, contract.functions.getPricePerFullShare().call()
        )

        return pricePerShare

    def displayWallet(self, farms):
        print(
            tabulate(
                farms,
                self.headers,
                floatfmt=(".f", ".4f", ".4f", ".2f"),
                tablefmt="simple",
            ),
            "\n",
        )
