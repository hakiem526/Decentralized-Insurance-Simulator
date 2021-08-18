from .PriceOracle import PriceOracle
from .utility.PriceImpactHandler import PriceImpactHandler

# This class maintains the AMM and the associated reserve values and price. Dex impliments a 3% transaction fee.
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

    # This private method determines price impact of buy transaction.
    # Price impact refers to the difference between the current market price and the expected fill price
    def __getPriceImpactOfInsrBuy(self, inputEthAmount):
        currInsrPrice = self.insrPrice
        amountInsrToReceive = self.getAmountInsrToReceive(inputEthAmount)
        insrPriceToHavePaid = inputEthAmount * self.ethPrice / amountInsrToReceive
        priceImpact = (insrPriceToHavePaid - currInsrPrice) / currInsrPrice
        return priceImpact
        
    # This private method determines price impact of sell transaction.
    # Price impact refers to the difference between the current market price and the expected fill price
    def __getPriceImpactOfInsrSell(self, inputInsrAmount):
        currInsrPrice = self.insrPrice
        amountEthToReceive = self.getAmountEthToReceive(inputInsrAmount)
        pricePerInsrToReceive = amountEthToReceive * self.ethPrice / inputInsrAmount
        priceImpact = (currInsrPrice - pricePerInsrToReceive) / currInsrPrice
        return priceImpact

    def getAmountInsrToReceive(self, inputEthAmount):
        inputEthAmountAfterFee = float(inputEthAmount) * 0.997 # 0.3% trx fee in ETH accounted
        updatedEthReserve = self.ethReserve + float(inputEthAmountAfterFee)
        updatedInsrReserve = self.constantProduct / updatedEthReserve
        outgoingInsr = self.insrReserve - updatedInsrReserve
        return outgoingInsr

    def getAmountEthToReceive(self, inputInsrAmount):
        updatedInsrReserve = self.insrReserve + float(inputInsrAmount)
        updatedEthReserve = self.constantProduct / updatedInsrReserve
        outgoingEth = self.ethReserve - updatedEthReserve
        outgoingEthAfterFee = outgoingEth * 0.997 # 0.3% trx fee in ETH accounted
        return outgoingEthAfterFee

    # This function processes buy transactions and updates reserves and price accordingly.
    # Function throws error if price impact > 10%, when buy amount too high.
    def transactBuyInsr(self, inputEthAmount):
        priceImpact = self.__getPriceImpactOfInsrBuy(inputEthAmount) 
        if (priceImpact < -0.1 or priceImpact > 0.1):
            return PriceImpactHandler(priceImpact)

        outgoingInsr = self.getAmountInsrToReceive(inputEthAmount)
        self.__updateEthReserve(inputEthAmount)
        self.__updateInsrReserve(outgoingInsr * -1)
        self.__updateInsrPrice()
        
        # generate receipt
        insrAverageCost = float(inputEthAmount) * self.ethPrice / outgoingInsr
        transactionReceipt = {'Type' : 'INSRBUY', 'Amount' : outgoingInsr, 'Price' : insrAverageCost, 'Total': inputEthAmount * self.ethPrice}
        return transactionReceipt

    # This function processes sell transactions and updates reserves and price accordingly.
    # Function throws error if price impact > 10% when sell amount too high.
    # Function throws error if price impact < 0 when sell amount too low.
    def transactSellInsr(self, inputInsrAmount):
        priceImpact = self.__getPriceImpactOfInsrSell(inputInsrAmount)
        if (priceImpact < -0.1 or priceImpact > 0.1):
            return PriceImpactHandler(priceImpact)
            
        outgoingEth = self.getAmountEthToReceive(inputInsrAmount)
        self.__updateInsrReserve(inputInsrAmount)
        self.__updateEthReserve(outgoingEth * -1)
        self.__updateInsrPrice()

        # generate receipt
        insrAverageCost = float(outgoingEth) * self.ethPrice / inputInsrAmount
        transactionReceipt = {'Type' : 'INSRSELL', 'Amount' : inputInsrAmount, 'Price' : insrAverageCost, 'Total' : outgoingEth * self.ethPrice}
        return transactionReceipt

    def __str__(self):
        return f'INSR AMM Details \n \t INSR Reserve: {self.insrReserve} \n \t ETH Reserve: {self.ethReserve} \n \t INSR Price: ${self.insrPrice} '
