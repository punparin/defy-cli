class Utilities:
    @staticmethod
    def formatBalance(web3, balance):
        return float(web3.fromWei(balance, 'ether'))

    @staticmethod
    def getTotal(tabulateBalances):
        total = 0

        for bal in tabulateBalances:
            total += sum([x[3] for x in bal])
        
        return total

    @staticmethod   
    def displayTotal(total):
        print("Total Balance: $%.2f" % (total))