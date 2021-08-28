from .Dex import Dex

# Parameters to set:
#   1. AMM parameters
#       a. Initial INSR reserve
#       b. Initial ETH reserve
#   2. MarketTaker parameters
#       a. Probabiliies for buy TKN, insure TKN, claim insurance, buy INSR, sell INSR

# This class presets the behaviour of actors and handles interactions between them
class Ecosystem:
    def __init__(self, dex, marketTakers):
        self.dex = Dex(dex)
        self.marketTakers = marketTakers

