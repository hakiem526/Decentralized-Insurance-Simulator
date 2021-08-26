from src.components.Ecosystem import Ecosystem
from src.components.Dex import Dex
from src.components.MarketTaker import MarketTaker

dex = Dex(40, 100000000)
x = MarketTaker(1)
print(dex)
print(x)
x.buyInsr(dex, 0.1)
print(dex)
print(x)