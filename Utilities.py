def formatBalance(web3, balance):
    return float(web3.fromWei(balance, 'ether'))

def getTotal(tabulateBalances):
    total = 0

    for bal in tabulateBalances:
        total += sum([x[3] for x in bal])
    
    return total
    
def displayTotal(total):
    print("Total Balance: $%.2f" % (total))