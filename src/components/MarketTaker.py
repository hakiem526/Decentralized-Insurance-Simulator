# Buy TKN - buy TKN using a certain percentage of ETH balance
# Buy INSR - buy INSR using a certain percentage of ETH balance
# Sell INSR - sell a certain amount of INSR balance for ETH
# Insure TKN - allocate a certain percentage of 
# Claim insurance - check for profitable insurance claim, claim if profitable, immediately sell for ETH.
class MarketTaker:

    totalNum = 0

    def __init__(self, ethBalance, probabilities):
        self.id = self.totalNum
        self.ethBalance = float(ethBalance)
        self.insrBalance = 0
        self.tknBalance = 0
        self.totalNum += 1

    # This function processes INSR buys from input Dex and updates local balances.
    # 
    def buyInsr(self, dex, ethAmount):
        incomingInsr = dex.getAmountInsrToReceive(ethAmount)
        if (incomingInsr):
            pass

    def sellInsr(self, dex, insrAmount):
        pass

    def buyTkn(self, dex, insrAmount):
        pass
