from .Dex import Dex
from ..utility.PriceOracle import PriceOracle
from typing import Dict

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

    # This private function returns the amount of ETH to be spent on INSR buy transaction
    # Possible proportions of ETH balance to be spent is hardcoded
    def __getAmountEthToSpend(self):
        assert(self.ethBalance > 0)
        proportions = [0.2, 0.3, 0.4, 0.5] 
        ethToSpend = random.choice(proportions) * self.ethBalance
        return ethToSpend

    # This private function returns the amount of INSR to be sold on INSR sell transaction
    # Possible proportions of INSR balance to be sold is hardcoded
    def __getAmountInsrToSell(self):
        assert self.insrBalance > 0, '0 INSR balance'
        proportions = [0.2, 0.3, 0.4, 0.5, 1]
        insrToSell = random.choice(proportions) * self.insrBalance
        return insrToSell

    def __updateEthBalance(self, delta):
        self.ethBalance += delta

    def __updateInsrBalance(self, delta):
        self.insrBalance += delta

    def __updateTokenBalance(self, delta):
        self.tknBalance += delta

    # This private function handles price impact of INSR buys from the perspective of a MarketTaker
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

    # This private function handles price impact INSR sells from the perspective of a MarketTaker
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

    # This private function processes INSR buys from input Dex and updates local balances
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
        

    # This private function processes INSR sells from input Dex and updates local balances
    # Price impact handlded before transaction processing
    def __sellSpecificAmountInsr(self, insrDex: Dex, insrAmount):
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

    # Called by Simulator for TKN buy transactions
    def buyTkn(self):
        # trx details
        ethToSpend = self.__getAmountEthToSpend()
        tknPrice = PriceOracle.getTknPrice()
        amountTknToReceive = ethToSpend * PriceOracle.ethPrice / tknPrice
        
        # update balances
        self.__updateEthBalance(ethToSpend * -1.0)
        self.__updateTokenBalance(amountTknToReceive)

        # trx receipt
        transactionReceipt = {'id': self.id, 'type' : 'TKNBUY', 'amount' : amountTknToReceive, 'price' : tknPrice, 'total': ethToSpend * PriceOracle.ethPrice}
        self.__printTrxReceiptPretty(transactionReceipt)
        print(self)

    # Called by Simulator for INSR buy transactions
    def buyInsr(self, insrDex: Dex):
        ethToSpend = self.__getAmountEthToSpend()
        self.__buyInsrWithSpecifiedEthAmount(insrDex, ethToSpend)
        print(self)

    # Called by Simulator for INSR sell transactions
    def sellInsr(self, insrDex: Dex):
        insrToSell = self.__getAmountInsrToSell()
        self.__sellSpecificAmountInsr(insrDex, insrToSell)
        print(self)

    # Used for buying specific amount of INSR for insurance
    def buySpecificInsrAmount(self, insrDex:Dex, amount):
        # TODO
        pass

    def __printTrxReceiptPretty(self, receipt: Dict):
        output = 'Trx receipt\n\tActor ID: ' + str(receipt.get('id')) + '\n\tType: ' + str(receipt.get('type')) + '\n\tAmount TKN: ' + str(receipt.get('amount')) + \
            '\n\tAvg price: $' + str(receipt.get('price')) + '\n\tTotal: $' + str(receipt.get('total'))
        print(output)

    def __str__(self):
        return 'MarketTaker' + '\n\tid: ' + str(self.id) + '\n\tETH balance: ' + str(self.ethBalance) + '\n\tINSR balance: ' + str(self.insrBalance) + \
            '\n\tTKN balance: ' + str(self.tknBalance)
