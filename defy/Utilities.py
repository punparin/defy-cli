class Utilities:
    @staticmethod
    def formatBalance(web3, balance):
        return float(web3.fromWei(balance, "ether"))

    @staticmethod
    def getTotal(tabulateBalances):
        total = 0

        for rawBal in tabulateBalances:
            bal = rawBal["bal"]
            typeBal = rawBal["type"]

            if typeBal in ["binance", "wallet", "fulcrum"]:
                total += sum([x[3] for x in bal])
            elif typeBal in ["valuedefi"]:
                total += sum([x[4] for x in bal])

        return total

    @staticmethod
    def displayTotal(total):
        print("Total Balance: $%.2f" % (total))
