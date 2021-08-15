from .Dex import Dex
from .MarketTaker import MarketTaker

# Parameters to set:
#   1. AMM parameters
#       a. Initial INSR reserve
#       b. Initial ETH reserve

class Ecosystem:
    def __init__(self, dex, marketTakers):
        self.dex = Dex(dex)
        self.marketTakers = marketTakers

