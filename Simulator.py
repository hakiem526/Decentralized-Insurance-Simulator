from src.components.Ecosystem import Ecosystem
from src.components.Dex import Dex

dex = Dex(20, 10000000)
print(dex.insrPrice)
print(dex.transactSellInsr(0.0000000000001))