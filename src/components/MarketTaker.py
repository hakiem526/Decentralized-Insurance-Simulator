from typing_extensions import ParamSpecKwargs


class MarketTaker:

    totalNum = 0

    def __init__(self, ethBalance):
        self.id = self.totalNum
        self.ethBalance = float(ethBalance)
        self.insrBalance = 0
        self.totalNum += 1

    # MarketTaker purchases INSR from input Dex
    def buyInsr(self, dex, ethAmount):
        incomingInsr = dex.getAmountInsrToReceive(ethAmount)
        if (incomingInsr):
            pass

    def sellInsr(self, dex, insrAmount):
        pass