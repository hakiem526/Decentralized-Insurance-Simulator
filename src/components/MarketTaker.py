from .Dex import Dex

# Buy TKN - buy TKN using a certain percentage of ETH balance
# Insure TKN - insure a certain percentage of TKN: Purchase sufficient amount of INSR for insurance -> insure on platform
# Claim insurance - check for profitable insurance claim, claim if profitable, immediately sell for ETH.
# Buy INSR - buy INSR using a certain percentage of ETH balance (for insuring TKN)
# Sell INSR - sell a certain amount of INSR balance for ETH (after claiming profitable insurance)
class MarketTaker:

    totalNum = 0

    def __init__(self, ethBalance, probabilities):
        assert probabilities.len() == 3
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
