from configparser import ConfigParser
import requests
import json
import os


class PriceFinder:
    def __init__(self):
        self.config = ConfigParser(os.environ)

        self.config.read("./config.ini")

        self.pancakePriceEndpoint = self.config["DEFAULT"]["pancake_price_endpoint"]
        self.oneInchChain56Endpoint = self.config["DEFAULT"][
            "oneinch_chain_56_endpoint"
        ]
        self.oneInchPriceEndpoint = self.config["DEFAULT"]["oneinch_price_endpoint"]

        with open("alias_tokens.json", "r") as aliasTokens_definition:
            self.aliasTokens = json.load(aliasTokens_definition)

        self.setupTokens()

    def setupTokens(self):
        pancakeTokens = self.getPancakeTokens()
        oneInchTokens = self.get1inchTokens(pancakeTokens["wbnb"])

        tokens = {**oneInchTokens, **pancakeTokens}

        self.tokens = self.getAliasTokens(tokens)

    def get1inchTokens(self, bnbPrice):
        tokens = {}

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
