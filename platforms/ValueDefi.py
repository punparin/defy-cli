from configparser import SafeConfigParser
from web3 import Web3
from tabulate import tabulate
from Utilities import *
from PriceFinder import PriceFinder
import json
import os
import requests

class ValueDefi:
    def __init__(self, priceFinder):
        self.config = SafeConfigParser(os.environ)

        self.config.read("config.ini")

        self.farmName = "ValueDefi"
        self.masterAddress = "0xd56339F80586c08B7a4E3a68678d16D37237Bd96"
        self.networkProvider = self.config["DEFAULT"]["network_provider"]
        self.valuedefiEndpoint = self.config["DEFAULT"]["valuedefi_endpoint"]
        self.headers = ["%s Farm" % self.farmName, "Balance", "Reward", "Balance ($)"]

        self.web3 = Web3(Web3.HTTPProvider(self.networkProvider))
        self.priceFinder = priceFinder

        with open("abis/valuedefi_abi.json", "r") as abi_definition:
            self.abi = json.load(abi_definition)

    def getPlatformFarms(self, walletAddress):
        platformFarms = []
        r = requests.get(self.valuedefiEndpoint)
        farms = r.json()["data"]

        for farm in farms:
            farmingContractAddress = farm["farmingContractAddress"]
            bal = self.getTokenBalance(farmingContractAddress, walletAddress)

            if bal != 0:
                pricePerShare = self.getTokenPricePerShare(farmingContractAddress)
                pairSymbol = farm["wantTokenSymbol"]
                mainTokenSymbol, pairTokenSymbol = pairSymbol.split("-")[0], pairSymbol.split("-")[1]
                mainTokenPrice = self.priceFinder.getTokenPrice(mainTokenSymbol)
                pairTokenPrice = self.priceFinder.getTokenPrice(pairTokenSymbol)
                reward = bal * pricePerShare - bal
                balInDollar = (bal + reward) * mainTokenPrice + (bal + reward) * pairTokenPrice
                
                platformFarms.append([pairSymbol, bal, reward, balInDollar])
        
        return platformFarms

    def getTokenBalance(self, contractAddress, walletAddress):
        contract = self.web3.eth.contract(abi=self.abi, address=Web3.toChecksumAddress(contractAddress))
        bal = formatBalance(self.web3, contract.functions.balanceOf(Web3.toChecksumAddress(walletAddress)).call())
        
        return bal

    def getTokenPricePerShare(self, contractAddress):
        contract = self.web3.eth.contract(abi=self.abi, address=Web3.toChecksumAddress(contractAddress))
        pricePerShare = formatBalance(self.web3, contract.functions.getPricePerFullShare().call())

        return pricePerShare

    def displayPlatformFarms(self, farms):
        print(tabulate(farms, self.headers, floatfmt=(".f", ".4f", ".4f", ".2f"), tablefmt="simple"), "\n")