from configparser import SafeConfigParser
from web3 import Web3
from tabulate import tabulate
from Utilities import *
from PriceFinder import PriceFinder
import requests
import json
import os

class Wallet:
    def __init__(self, priceFinder):
        self.config = SafeConfigParser(os.environ)

        self.config.read("config.ini")

        self.networkProvider = self.config["DEFAULT"]["network_provider"]
        self.transactionEndpoint = self.config["DEFAULT"]["bscscan_transaction_endpoint"]
        self.headers = ["Token", "Price", "Balance", "Balance ($)"]

        self.web3 = Web3(Web3.HTTPProvider(self.networkProvider))
        self.priceFinder = priceFinder

        with open("abis/wallet_abi.json", "r") as abi_definition:
            self.abi = json.load(abi_definition)

    def getTokenBalance(self, contractAddress, walletAddress):
        contract = self.web3.eth.contract(abi=self.abi, address=Web3.toChecksumAddress(contractAddress))

        return formatBalance(self.web3, contract.functions.balanceOf(walletAddress).call())

    def getTokenName(self, contractAddress):
        contract = self.web3.eth.contract(abi=self.abi, address=Web3.toChecksumAddress(contractAddress))

        return contract.functions.name().call()

    def getSymbol(self, contractAddress):
        contract = self.web3.eth.contract(abi=self.abi, address=Web3.toChecksumAddress(contractAddress))
        
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

            if bal == 0 or (hideSmallBal and bal < 0.0001):
                continue
            
            price = self.priceFinder.getTokenPrice(symbol)

            if price == 0:
                continue

            balInDollar = bal * price

            wallet.append([symbol, price, bal, balInDollar])

        total = sum([x[3] for x in wallet])
        
        return wallet

    def sortingKey(self, e):
        return str(e[3])

    def formatTable(self, wallet):
        newWallet = []

        for i in range(len(wallet) - 1):
            item = wallet[i]

            if type(item[1]) != str:
                newWallet.append([item[0], format(item[1], ".2f"), format(item[2], ".4f"), format(item[3], ".2f")])
            else:
                newWallet.append([item[0], item[1], format(item[2], ".4f"), item[3]])

        total = wallet[-1]

        newWallet.append([total[0], total[1], total[2], format(total[3], ".2f")])

        return newWallet

    def displayWallet(self, wallet):
        print(tabulate(wallet, self.headers, floatfmt=(".f", ".2f", ".4f", ".2f"), tablefmt="simple"), "\n")