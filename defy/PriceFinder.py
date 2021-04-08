from configparser import SafeConfigParser
import requests
import json
import os

class PriceFinder:
    def __init__(self):
        self.config = SafeConfigParser(os.environ)

        self.config.read("config.ini")

        self.pancakeEndpoint = self.config["DEFAULT"]["pancake_endpoint"]

        self.tokens = self.setupTokens()

    def setupTokens(self):
        r = requests.get(self.pancakeEndpoint)
        tokens = r.json()["prices"]

        for k, v in tokens.items():
            tokens[k] = float(v)

        formattedTokens = dict((k.lower(), v) for k,v in tokens.items())

        return formattedTokens

    def getTokenPrice(self, symbol):
        return self.tokens.get(symbol.lower(), 0)