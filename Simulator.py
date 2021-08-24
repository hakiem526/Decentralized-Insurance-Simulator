from src.components.Ecosystem import Ecosystem
from src.components.Dex import Dex

dex = Dex(20, 10000000)
print(dex.getCostOfInsrBuyInEth(100000) * dex.ethPrice)
print(dex.transactBuyInsr(dex.getCostOfInsrBuyInEth(100000)))