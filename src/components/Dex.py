from typing import Dict
from ..utility.PriceOracle import PriceOracle

# This class maintains the AMM and the associated reserve values and price. Dex does not impliments a transaction fee.
# Buy or sell transactions that will have too high a price impact will not be processed.
class Dex:

    # Constant price of ETH to simplify ecosystem simulator
    ethPrice = PriceOracle.ethPrice

    def __init__(self, ethReserve, insrReserve):
        # evaluate reserve amounts
        self.ethReserve = float(ethReserve)
        self.insrReserve = float(insrReserve)

        # evaluate constant product for AMM
        self.constantProduct = ethReserve * insrReserve

        # evaluate listing price
        self.insrPrice = (ethReserve / insrReserve) * self.ethPrice

    def __updateInsrPrice(self):
        self.insrPrice = (float(self.ethReserve) / float(self.insrReserve)) * self.ethPrice

    def __updateInsrReserve(self, delta):
        self.insrReserve += float(delta)

    def __updateEthReserve(self, delta): 
        self.ethReserve += float(delta)

    # This function determines price impact of buy transaction. Call this method before transactBuyInsr()
    # Price impact refers to the difference between the current market price and the expected fill price
    def getPriceImpactOfInsrBuy(self, inputEthAmount):
        assert inputEthAmount > 0, 'Cannot input 0 ETH'

        currInsrPrice = self.insrPrice
        amountInsrToReceive = self.getAmountInsrToReceive(inputEthAmount)
        insrPriceToHavePaid = inputEthAmount * self.ethPrice / amountInsrToReceive
        priceImpact = (insrPriceToHavePaid - currInsrPrice) / currInsrPrice
        return priceImpact
        
    # This function determines price impact of sell transaction. Call this method before transactSellInsr()
    # Price impact refers to the difference between the current market price and the expected fill price
    def getPriceImpactOfInsrSell(self, inputInsrAmount):
        assert inputInsrAmount > 0, 'Cannot input 0 INSR'

        currInsrPrice = self.insrPrice
        amountEthToReceive = self.getAmountEthToReceive(inputInsrAmount)
        pricePerInsrToReceive = amountEthToReceive * self.ethPrice / inputInsrAmount
        priceImpact = (currInsrPrice - pricePerInsrToReceive) / currInsrPrice
        return priceImpact

    # This function returns output INSR amount given specified ETH sell amount
    def getAmountInsrToReceive(self, inputEthAmount):
        assert inputEthAmount > 0, 'Cannot input 0 ETH'

        inputEthAmountAfterFee = float(inputEthAmount)
        updatedEthReserve = self.ethReserve + float(inputEthAmountAfterFee)
        updatedInsrReserve = self.constantProduct / updatedEthReserve
        outgoingInsr = self.insrReserve - updatedInsrReserve
        return outgoingInsr

    # This function returns output ETH amount given specified INSR sell amount
    def getAmountEthToReceive(self, inputInsrAmount):
        assert inputInsrAmount > 0, 'Cannot input 0 INSR'

        updatedInsrReserve = self.insrReserve + float(inputInsrAmount)
        updatedEthReserve = self.constantProduct / updatedInsrReserve
        outgoingEth = self.ethReserve - updatedEthReserve
        outgoingEthAfterFee = outgoingEth
        return outgoingEthAfterFee

    # This function returns cost of buying a specific amount of INSR in ETH
    # Use this function to process buys of specific amount of INSR
    def getCostOfInsrBuyInEth(self, expectedOutputInsr):
        assert expectedOutputInsr > 0, 'Cannot buy 0 INSR'
        assert expectedOutputInsr < self.insrReserve, 'Cannot buy all reserves'
        
        costInEth = self.constantProduct / (self.insrReserve - expectedOutputInsr) - self.ethReserve
        return costInEth

    # This function processes buy transactions and updates reserves and price accordingly. Returns dictionary of transaction details
    # Function throws exception if price impact > 10%, when buy amount too high
    # Function throws exception if price impact < -10%, when buy amount too low
    def transactBuyInsr(self, inputEthAmount):
        priceImpact = self.getPriceImpactOfInsrBuy(inputEthAmount) 
        assert priceImpact < 0.1 and priceImpact > -0.1

        outgoingInsr = self.getAmountInsrToReceive(inputEthAmount)
        self.__updateEthReserve(inputEthAmount)
        self.__updateInsrReserve(outgoingInsr * -1)
        self.__updateInsrPrice()
        
        # generate receipt
        insrAverageCost = float(inputEthAmount) * self.ethPrice / outgoingInsr
        transactionReceipt = {'type' : 'INSRBUY', 'amount' : outgoingInsr, 'price' : insrAverageCost, 'total': inputEthAmount * self.ethPrice}
        self.__printTrxReceiptPretty(transactionReceipt)
        return transactionReceipt

    # This function processes sell transactions and updates reserves and price accordingly. Returns dictionary of transaction details
    # Function throws exception if price impact > 10%, when sell amount too high
    # Function throws exception if price impact < -10%, when sell amount too low
    def transactSellInsr(self, inputInsrAmount):
        priceImpact = self.getPriceImpactOfInsrSell(inputInsrAmount)
        assert priceImpact < 0.1 and priceImpact > -0.1

        outgoingEth = self.getAmountEthToReceive(inputInsrAmount)
        self.__updateInsrReserve(inputInsrAmount)
        self.__updateEthReserve(outgoingEth * -1)
        self.__updateInsrPrice()

        # generate receipt
        insrAverageCost = float(outgoingEth) * self.ethPrice / inputInsrAmount
        transactionReceipt = {'type' : 'INSRSELL', 'amount' : inputInsrAmount, 'price' : insrAverageCost, 'total' : outgoingEth * self.ethPrice}
        self.__printTrxReceiptPretty(transactionReceipt)
        return transactionReceipt

    def __printTrxReceiptPretty(self, receipt: Dict):
        output = 'Trx receipt\n\t' + 'Type: ' + str(receipt.get('type')) + '\n\tAmount INSR: ' + str(receipt.get('amount')) + \
            '\n\tAvg price: $' + str(receipt.get('price')) + '\n\tTotal: $' + str(receipt.get('total'))
        print(output)

    def __str__(self):
        return 'INSR AMM \n\t INSR reserve: ' + str(self.insrReserve) + ' \n\t ETH reserve: ' + str(self.ethReserve) +  \
            '\n\t INSR price: $' + str(self.insrPrice)
