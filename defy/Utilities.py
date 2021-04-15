class Utilities:
    @staticmethod
    def formatBalance(web3, balance):
        return float(web3.fromWei(balance, "ether"))

    @staticmethod
    def getTotal(balances):
        total = 0

        for bal in balances:
            total += sum([x["balInDollar"] for x in bal])

        return total

    @staticmethod
    def displayTotal(total):
        print("Total Balance: $%.2f" % (total))
