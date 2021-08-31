from .Dex import Dex
from ..utility.PriceOracle import PriceOracle

# Buy TKN - buy TKN using a certain percentage of ETH balance
# Insure TKN - insure a certain percentage of TKN: Purchase sufficient amount of INSR for insurance -> insure on platform
# Claim insurance - check for profitable insurance claim, claim if profitable, immediately sell for ETH
# Buy INSR - buy INSR using a certain percentage of ETH balance (for insuring TKN)
# Sell INSR - sell a certain amount of INSR balance for ETH (after claiming profitable insurance)

import random

class MarketTaker:

    def __init__(self, id, ethBalance):
        self.id = id
        self.ethBalance = float(ethBalance)
        self.insrBalance = 0.0
        self.tknBalance = 0.0

    # This function returns the amount of ETH to be spent on INSR buy transaction
    # Possible proportions of ETH balance to be spent is hardcoded
    def __getAmountEthToSpend(self):
        proportions = [0.2, 0.3, 0.4, 0.5] 
        ethToSpend = random.choice(proportions) * self.ethBalance
        print(ethToSpend)
        return ethToSpend

    def __updateEthBalance(self, delta):
        self.ethBalance += delta

    def __updateInsrBalance(self, delta):
        self.insrBalance += delta

    def __updateTokenBalance(self, delta):
        self.tknBalance += delta

    # This function handles price impact of INSR buys from the perspective of a MarketTaker
    # Input ETH amounts are scaled up or down by 10% until price impact of transaction falls between -10% and 10%
    # Function will return (initial) ethAmount if handling price impact results in updatedEthAmount of > ethBalance
    def __handlePriceImpactOfInsrBuy(self, insrDex: Dex, ethAmount):
        priceImpact = insrDex.getPriceImpactOfInsrBuy(ethAmount)
        updatedEthAmount = ethAmount

        while(priceImpact > 0.1 or priceImpact < -0.1):
            if(priceImpact > 0.1):
                updatedEthAmount *= 0.90
            if(priceImpact < -0.1):
                updatedEthAmount *= 1.10
            priceImpact = insrDex.getPriceImpactOfInsrBuy(updatedEthAmount)

        if updatedEthAmount > self.ethBalance:
            updatedEthAmount = ethAmount

        return updatedEthAmount

    # This function handles price impact INSR sells from the perspective of a MarketTaker
    # Input INSR amounts are scaled up or down by 10% until price impact of transaction falls between -10% and 10%
    # Function will return (initial) insrAmount if handling price impact results in updatedInsrAmount of > insrBalance
    def __handlePriceImpactOfInsrSell(self, insrDex: Dex, insrAmount):
        priceImpact = insrDex.getPriceImpactOfInsrSell(insrAmount)
        updatedInsrAmount = insrAmount

        while(priceImpact > 0.1 or priceImpact < -0.1):
            if (priceImpact > 0.1):
                updatedInsrAmount *= 0.90
            if(priceImpact < -0.1):
                updatedInsrAmount *= 1.10
            priceImpact = insrDex.getPriceImpactOfInsrSell(updatedInsrAmount)

        if updatedInsrAmount > self.insrBalance:
            updatedInsrAmount = insrAmount

        return updatedInsrAmount

    # This function processes INSR buys from input Dex and updates local balances
    # Price impact handled before transaction processing
    def __buyInsrWithSpecifiedEthAmount(self, insrDex: Dex, ethAmount):
        assert ethAmount <= self.ethBalance, 'Input ETH > balance'
        
        # handle price impact
        updatedEthAmount = self.__handlePriceImpactOfInsrBuy(insrDex, ethAmount)
        assert updatedEthAmount <= self.ethBalance, 'Input ETH > balance'

        # process DEX transaction 
        incomingInsr = insrDex.getAmountInsrToReceive(updatedEthAmount)
        insrDex.transactBuyInsr(self.id, updatedEthAmount)
            
        # update balances
        self.__updateEthBalance(updatedEthAmount * -1.0)
        self.__updateInsrBalance(incomingInsr)
        

    # This function processes INSR sells from input Dex and updates local balances
    # Price impact handlded before transaction processing
    def sellInsr(self, insrDex: Dex, insrAmount):
        assert insrAmount <= self.insrBalance, 'Input INSR > balance'
        
        # handle price impact
        updatedInsrAmount = self.__handlePriceImpactOfInsrSell(insrDex, insrAmount)
        assert updatedInsrAmount <= self.insrBalance
        
        # process DEX transaction
        incomingEth = insrDex.getAmountEthToReceive(updatedInsrAmount)
        insrDex.transactSellInsr(self.id, updatedInsrAmount)

        # update balances
        self.__updateInsrBalance(updatedInsrAmount * -1.0)
        self.__updateEthBalance(incomingEth)

    def buyTkn(self, tknDex, insrAmount):
        ethToSpend = self.ethBalance * 1
        tknPrice = PriceOracle.getTknPrice()

    def buyInsr(self, insrDex: Dex):
        ethToSpend = self.__getAmountEthToSpend()
        self.__buyInsrWithSpecifiedEthAmount(insrDex, ethToSpend)

    def __str__(self):
        return 'MarketTaker' + '\n\tid: ' + str(self.id) + '\n\tETH balance: ' + str(self.ethBalance) + '\n\tINSR balance: ' + str(self.insrBalance) + \
            '\n\tTKN balance: ' + str(self.tknBalance)
