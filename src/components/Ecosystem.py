from .Dex import Dex

# Parameters to set:
#   1. AMM parameters
#       a. Initial INSR reserve
#       b. Initial ETH reserve

# This class presets the behaviour of actors and handles interactions between them
class Ecosystem:
    def __init__(self, dex, marketTakers):
        self.dex = Dex(dex)
        self.marketTakers = marketTakers

