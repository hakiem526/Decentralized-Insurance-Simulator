from src.components.Ecosystem import Ecosystem
from src.components.Dex import Dex
from src.components.MarketTaker import MarketTaker

# init Dex
dex = Dex(40, 100000000)

# init MarketTakers
currId = 0
marketTakers = []
for i in range (10):
    marketTakers.append(MarketTaker(currId, 10))
    currId += 1

# init Ecosystem
ecosystem = Ecosystem(dex, marketTakers)

# run sim
ecosystem.run(5)