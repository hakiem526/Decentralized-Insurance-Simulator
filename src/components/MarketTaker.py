from .Dex import Dex
from ..utility.PriceOracle import PriceOracle

# Buy TKN - buy TKN using a certain percentage of ETH balance
# Insure TKN - insure a certain percentage of TKN: Purchase sufficient amount of INSR for insurance -> insure on platform
# Claim insurance - check for profitable insurance claim, claim if profitable, immediately sell for ETH.
# Buy INSR - buy INSR using a certain percentage of ETH balance (for insuring TKN)
# Sell INSR - sell a certain amount of INSR balance for ETH (after claiming profitable insurance)

class MarketTaker:

    totalNum = 0

    def __init__(self, ethBalance):
        # probabilities for each action? 

        self.id = self.totalNum
        self.ethBalance = float(ethBalance)
        self.insrBalance = 0.0
        self.tknBalance = 0.0
        self.totalNum += 1
        # self.probabilities = probabilities

    def __getAmountEthToSpend(self): 
        pass

    def __updateEthBalance(self, delta):
        self.ethBalance += delta

    def __updateInsrBalance(self, delta):
        self.insrBalance += delta

    def __updateTokenBalance(self, delta):
        self.tknBalance += delta

    # This function processes INSR buys from input Dex and updates local balances.
    def buyInsr(self, insrDex: Dex, ethAmount):
        assert ethAmount <= self.ethBalance, 'Input ETH > balance'
        # handle price impact?
        
        incomingInsr = insrDex.getAmountInsrToReceive(ethAmount)
        insrDex.transactBuyInsr(ethAmount)

        # update balances
        self.__updateEthBalance(ethAmount * -1.0)
        self.__updateInsrBalance(incomingInsr)

    # This function processes INSR buys from input Dex and updates local balances.
    def sellInsr(self, insrDex: Dex, insrAmount):
        assert insrAmount <= self.insrBalance, 'Input INSR > balance'
        # handle price impact?
        
        incomingEth = insrDex.getAmountEthToReceive(insrAmount)
        insrDex.transactSellInsr(insrAmount)

        # update balances
        self.__updateInsrBalance(insrAmount * -1.0)
        self.__updateEthBalance(incomingEth)

    def buyTkn(self, tknDex, insrAmount):
        ethToSpend = self.ethBalance * 1
        tknPrice = PriceOracle.getTknPrice()

    def __str__(self):
        return 'MarketTaker' + '\n\tid: ' + str(self.id) + '\n\tETH balance: ' + str(self.ethBalance) + '\n\tINSR balance: ' + str(self.insrBalance) + \
            '\n\tTKN balance: ' + str(self.tknBalance)
