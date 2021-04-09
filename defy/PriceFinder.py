from configparser import SafeConfigParser
import requests
import json
import os

class PriceFinder:
    def __init__(self):
        self.config = SafeConfigParser(os.environ)

        self.config.read("config.ini")

        self.pancakeEndpoint = self.config["DEFAULT"]["pancake_endpoint"]

        with open("alias_tokens.json", "r") as aliasTokens_definition:
            self.aliasTokens = json.load(aliasTokens_definition)

        self.tokens = self.setupTokens()
        self.setupAliasTokens()

    def setupTokens(self):
        r = requests.get(self.pancakeEndpoint)
        tokens = r.json()["prices"]

        for k, v in tokens.items():
            tokens[k] = float(v)

        formattedTokens = dict((k.lower(), v) for k,v in tokens.items())

        return formattedTokens

    def setupAliasTokens(self):
        for key in self.aliasTokens:
            value = self.aliasTokens[key]
            self.tokens[key] = self.tokens[value]

    def getTokenPrice(self, symbol):
        return self.tokens.get(symbol.lower(), 0)