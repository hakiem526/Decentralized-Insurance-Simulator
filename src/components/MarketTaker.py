from .Dex import Dex
from ..utility.PriceOracle import PriceOracle

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
        self.insrBalance = 0.0
        self.tknBalance = 0.0
        self.totalNum += 1
        self.probabilities = probabilities

    # This function processes INSR buys from input Dex and updates local balances.
    # 
    def buyInsr(self, insrDex: Dex, ethAmount):
        insrDex.transactBuyInsr(ethAmount)

    def sellInsr(self, dex: Dex, insrAmount):
        pass

    def buyTkn(self, tknDex, insrAmount):
        ethToSpend = self.ethBalance * 1
        tknPrice = PriceOracle.getTknPrice()

    def getAmountEthToSpend(self): 
        pass