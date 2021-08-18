from src.components.Ecosystem import Ecosystem
from src.components.Dex import Dex

dex = Dex(20, 10000000)
for i in range(1, 11):
    currPrice = dex.insrPrice
    print(dex.transactBuyInsr(0.4))
    updatedPrice = dex.insrPrice
    priceChange = (updatedPrice - currPrice) / currPrice * 100
    print('Price change: %', priceChange)

for i in range(1, 11):
    currPrice = dex.insrPrice
    dex.transactSellInsr(100000)
    updatedPrice = dex.insrPrice
    priceChange = (updatedPrice - currPrice) / currPrice * 100
    print('Price change: %', priceChange)

