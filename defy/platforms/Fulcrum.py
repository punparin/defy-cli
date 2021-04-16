from configparser import ConfigParser
from web3 import Web3
from tabulate import tabulate
from defy.Utilities import Utilities
from defy.PriceFinder import PriceFinder
import json
import os
import requests


class Fulcrum:
    def __init__(self, priceFinder):
        self.config = ConfigParser(os.environ)

        self.config.read("./config.ini")

        self.platformName = "Fulcrum"
        self.contractAddress = "0x1FDCA2422668B961E162A8849dc0C2feaDb58915"
        self.networkProvider = self.config["DEFAULT"]["network_provider"]
        self.headers = [
            self.platformName,
            "Deposit",
            "Reward (BGOV)",
            "Balance ($)",
        ]

        self.web3 = Web3(Web3.HTTPProvider(self.networkProvider))
        self.priceFinder = priceFinder

        with open("abis/fulcrum_abi.json", "r") as abi_definition:
            self.fulcrumAbi = json.load(abi_definition)

        with open("abis/token_abi.json", "r") as abi_definition:
            self.tokenAbi = json.load(abi_definition)

        with open("abis/itoken_abi.json", "r") as abi_definition:
            self.itokenAbi = json.load(abi_definition)

    def getWallet(self, walletAddress, hideSmallBal=True):
        platformFarms = []

        contract = self.web3.eth.contract(
            abi=self.fulcrumAbi, address=Web3.toChecksumAddress(self.contractAddress)
        )
        tokens = contract.functions.getOptimisedUserInfos(
            Web3.toChecksumAddress(walletAddress)
        ).call()
        pools = self.getPoolInfos()
        rewards = self.getReward(walletAddress)

        for i in range(len(tokens)):
            token = tokens[i]
            pool = pools[i]
            deposit = Utilities.formatBalance(self.web3, token[0])

            if deposit != 0:
                reward = Utilities.formatBalance(self.web3, rewards[i])
                iTokenAddress = pool[0]

                try:
                    tokenAddress = self.getLoanTokenAddress(iTokenAddress)
                    symbol = self.getSymbol(tokenAddress)
                except Exception:
                    symbol = self.getSymbol(iTokenAddress)

                tokenPrice = self.priceFinder.getTokenPrice(symbol)
                rewardPrice = self.priceFinder.getTokenPrice("BGOV")
                balInDollar = deposit * tokenPrice + reward * rewardPrice

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

    def getPoolInfos(self):
        contract = self.web3.eth.contract(
            abi=self.fulcrumAbi, address=Web3.toChecksumAddress(self.contractAddress)
        )

        return contract.functions.getPoolInfos().call()

    def getLoanTokenAddress(self, contractAddress):
        contract = self.web3.eth.contract(
            abi=self.itokenAbi, address=Web3.toChecksumAddress(contractAddress)
        )

        return contract.functions.loanTokenAddress().call()

    def getSymbol(self, contractAddress):
        contract = self.web3.eth.contract(
            abi=self.tokenAbi, address=Web3.toChecksumAddress(contractAddress)
        )

        return contract.functions.symbol().call()

    def getReward(self, walletAddress):
        contract = self.web3.eth.contract(
            abi=self.fulcrumAbi, address=Web3.toChecksumAddress(self.contractAddress)
        )

        return contract.functions.getPendingBGOV(
            Web3.toChecksumAddress(walletAddress)
        ).call()

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
