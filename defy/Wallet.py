from configparser import ConfigParser
from web3 import Web3
from tabulate import tabulate
from defy.Utilities import Utilities
from defy.PriceFinder import PriceFinder
import requests
import json
import os


class Wallet:
    def __init__(self, priceFinder):
        self.config = ConfigParser()

        self.config.read("./config.ini")

        self.networkProvider = self.config["DEFAULT"]["network_provider"]
        self.transactionEndpoint = self.config["DEFAULT"][
            "bscscan_transaction_endpoint"
        ]
        self.headers = ["Wallet", "Price", "Balance", "Balance ($)"]

        self.web3 = Web3(Web3.HTTPProvider(self.networkProvider))
        self.priceFinder = priceFinder

        with open("abis/token_abi.json", "r") as abi_definition:
            self.tokenAbi = json.load(abi_definition)

    def getTokenBalance(self, contractAddress, walletAddress):
        contract = self.web3.eth.contract(
            abi=self.tokenAbi, address=Web3.toChecksumAddress(contractAddress)
        )

        return Utilities.formatBalance(
            self.web3, contract.functions.balanceOf(walletAddress).call()
        )

    def getTokenName(self, contractAddress):
        contract = self.web3.eth.contract(
            abi=self.tokenAbi, address=Web3.toChecksumAddress(contractAddress)
        )

        return contract.functions.name().call()

    def getSymbol(self, contractAddress):
        contract = self.web3.eth.contract(
            abi=self.tokenAbi, address=Web3.toChecksumAddress(contractAddress)
        )

        return contract.functions.symbol().call()

    def getWalletTokens(self, walletAddress):
        transactions = {}
        endpoint = self.transactionEndpoint + "&address=" + walletAddress
        r = requests.get(endpoint)

        for item in r.json()["result"]:
            transactions[item["tokenSymbol"]] = item["contractAddress"]

        return transactions

    def getWallet(self, walletAddress, hideSmallBal=True):
        wallet = []
        tokens = self.getWalletTokens(walletAddress)
        walletAddress = Web3.toChecksumAddress(walletAddress)

        for symbol in tokens:
            bal = self.getTokenBalance(tokens[symbol], walletAddress)

            if bal != 0:
                price = self.priceFinder.getTokenPrice(symbol)
                balInDollar = bal * price

                if hideSmallBal and balInDollar < 1:
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
