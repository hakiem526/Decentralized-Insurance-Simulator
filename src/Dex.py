class Dex:
    # Constant price of ETH to simplify ecosystem simulator
    ethPrice = 3000.0

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

    def getAmountInsrToReceive(self, inputEthAmount):
        updatedEthReserve = self.ethReserve + float(inputEthAmount)
        updatedInsrReserve = self.constantProduct / updatedEthReserve
        outgoingInsr = self.insrReserve - updatedInsrReserve
        return outgoingInsr

    def getAmountEthToReceive(self, inputInsrAmount):
        updatedInsrReserve = self.insrReserve + float(inputInsrAmount)
        updatedEthReserve = self.constantProduct / updatedInsrReserve
        outgoingEth = self.ethReserve - updatedEthReserve
        return outgoingEth

    def buyInsr(self, inputEthAmount):
        outgoingInsr = self.getAmountInsrToReceive(inputEthAmount)
        self.__updateEthReserve(inputEthAmount)
        self.__updateInsrReserve(outgoingInsr * -1)
        self.__updateInsrPrice()
        
        # generate receipt
        insrAverageCost = float(inputEthAmount) * self.ethPrice / outgoingInsr
        transactionReceipt = {'Type' : 'INSRBUY', 'Amount' : outgoingInsr, 'Price' : insrAverageCost}
        return transactionReceipt

    def sellInsr(self, inputInsrAmount):
        outgoingEth = self.getAmountEthToReceive(inputInsrAmount)
        self.__updateInsrReserve(inputInsrAmount)
        self.__updateEthReserve(outgoingEth * -1)
        self.__updateInsrPrice()

        # generate receipt
        insrAverageCost = float(outgoingEth) * self.ethPrice / inputInsrAmount
        transactionReceipt = {'Type' : 'INSRSELL', 'Amount' : inputInsrAmount, 'Price' : insrAverageCost}

    def __str__(self):
        return f'INSR AMM Details \n \t INSR Reserve: {self.insrReserve} \n \t ETH Reserve: {self.ethReserve} \n \t INSR Price: ${self.insrPrice} '
