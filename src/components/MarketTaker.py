from .Dex import Dex
from ..utility.PriceOracle import PriceOracle

# Buy TKN - buy TKN using a certain percentage of ETH balance
# Insure TKN - insure a certain percentage of TKN: Purchase sufficient amount of INSR for insurance -> insure on platform
# Claim insurance - check for profitable insurance claim, claim if profitable, immediately sell for ETH
# Buy INSR - buy INSR using a certain percentage of ETH balance (for insuring TKN)
# Sell INSR - sell a certain amount of INSR balance for ETH (after claiming profitable insurance)

class MarketTaker:

    totalNum = 0

    def __init__(self, ethBalance):
        self.id = self.totalNum
        self.ethBalance = float(ethBalance)
        self.insrBalance = 0.0
        self.tknBalance = 0.0
        self.totalNum += 1

    def __getAmountEthToSpend(self): 
        pass

    def __updateEthBalance(self, delta):
        self.ethBalance += delta

    def __updateInsrBalance(self, delta):
        self.insrBalance += delta

    def __updateTokenBalance(self, delta):
        self.tknBalance += delta

    # This function handles price impact from the perspective of a MarketTaker
    # Input ETH amounts are scaled up or down by 10% until price impact of transaction falls between -10% and 10%
    # Function will return (initial) ethAmount if handling price impact results in updatedEthAmount of > ethBalance
    def __handlePriceImpactOfInsrBuy(self, insrDex: Dex, ethAmount):
        priceImpact = insrDex.getPriceImpactOfInsrBuy(ethAmount)
        updatedEthAmount = ethAmount

        while(priceImpact > 0.1 or priceImpact < -0.1):
            if(priceImpact > 0.1):
                updatedEthAmount *= 0.90
            if(priceImpact < -0.1):
                updatedEthAmount *= 1.1
            priceImpact = insrDex.getPriceImpactOfInsrBuy(updatedEthAmount)

        if updatedEthAmount > self.ethBalance:
            updatedEthAmount = ethAmount

        print('Updated ETH amount:' + str(updatedEthAmount))
        return updatedEthAmount

    # This function processes INSR buys from input Dex and updates local balances
    # Price impact handled before transaction processing
    def buyInsr(self, insrDex: Dex, ethAmount):
        assert ethAmount <= self.ethBalance, 'Input ETH > balance'
        
        # handle price impact
        updatedEthAmount = self.__handlePriceImpactOfInsrBuy(insrDex, ethAmount)
        assert updatedEthAmount <= self.ethBalance, 'Input ETH > balance'

        # process DEX transaction 
        incomingInsr = insrDex.getAmountInsrToReceive(updatedEthAmount)
        insrDex.transactBuyInsr(updatedEthAmount)
            
        # update balances
        self.__updateEthBalance(updatedEthAmount * -1.0)
        self.__updateInsrBalance(incomingInsr)
        

    # This function processes INSR buys from input Dex and updates local balances
    def sellInsr(self, insrDex: Dex, insrAmount):
        assert insrAmount <= self.insrBalance, 'Input INSR > balance'
        # handle price impact
        
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
