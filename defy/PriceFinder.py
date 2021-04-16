from defy.Utilities import Utilities
from configparser import ConfigParser
from web3 import Web3
import requests
import json
import os


class PriceFinder:
    def __init__(self):
        self.config = ConfigParser(os.environ)

        self.config.read("./config.ini")

        self.chainlinkPriceFeedAddress = "0x0567F2323251f0Aab15c8dFb1967E4e8A7D42aeE"
        self.networkProvider = self.config["DEFAULT"]["network_provider"]
        self.pancakePriceEndpoint = self.config["DEFAULT"]["pancake_price_endpoint"]
        self.oneInchChain56Endpoint = self.config["DEFAULT"][
            "oneinch_chain_56_endpoint"
        ]
        self.oneInchPriceEndpoint = self.config["DEFAULT"]["oneinch_price_endpoint"]

        self.web3 = Web3(Web3.HTTPProvider(self.networkProvider))

        with open("alias_tokens.json", "r") as aliasTokens_definition:
            self.aliasTokens = json.load(aliasTokens_definition)

        with open("abis/chainlink_abi.json", "r") as abi_definition:
            self.chainlinkAbi = json.load(abi_definition)

        self.setupTokens()

    def merge(self, dicts):
        result = dict()

        for x in dicts:
            result.update(x)

        return result

    def setupTokens(self):
        pancakeTokens = self.getPancakeTokens()
        oneInchTokens = self.get1inchTokens()

        tokens = self.merge([pancakeTokens, oneInchTokens])

        self.tokens = self.getAliasTokens(tokens)

    def getBNBPrice(self):
        contract = self.web3.eth.contract(
            abi=self.chainlinkAbi,
            address=Web3.toChecksumAddress(self.chainlinkPriceFeedAddress),
        )
        decimals = contract.functions.decimals().call()
        latestRoundData = contract.functions.latestRoundData().call()
        price = self.formatBalance(latestRoundData[1], decimals)

        return price

    def get1inchTokens(self):
        tokens = {}
        bnbPrice = self.getBNBPrice()

        r = requests.get(self.oneInchPriceEndpoint)
        addrTokens = r.json()

        r = requests.get(self.oneInchChain56Endpoint)
        tokensInfo = r.json()

        for addr in addrTokens:
            price = int(addrTokens[addr])
            try:
                symbol = tokensInfo[addr]["symbol"]
                decimals = int(tokensInfo[addr]["decimals"])
                tokens[symbol] = self.formatBalance(price, decimals) * bnbPrice
            except KeyError:
                pass
        tokens["wbnb"] = bnbPrice

        formattedTokens = dict((k.lower(), v) for k, v in tokens.items())

        return formattedTokens

    def getPancakeTokens(self):
        r = requests.get(self.pancakePriceEndpoint)
        tokens = r.json()["prices"]

        for k, v in tokens.items():
            tokens[k] = float(v)

        formattedTokens = dict((k.lower(), v) for k, v in tokens.items())

        return formattedTokens

    def getAliasTokens(self, tokens):
        for key in self.aliasTokens:
            value = self.aliasTokens[key]
            tokens[key] = tokens[value]

        return tokens

    def getTokenPrice(self, symbol):
        return self.tokens.get(symbol.lower(), 0)

    def formatBalance(self, bal, decimals):
        return bal * 10 ** -decimals
