from .Dex import Dex
from .MarketTaker import MarketTaker
from typing import List
import random

# Parameters to set:
#   1. AMM parameters
#       a. Initial INSR reserve
#       b. Initial ETH reserve
#   2. MarketTaker parameters
#       a. Probabiliies for buy TKN, insure TKN, claim insurance, buy INSR, sell INSR

# Note: Must handle exceptions from actors

# This class presets the behaviour of actors and handles interactions between them
class Ecosystem:
    def __init__(self, dex: Dex, marketTakers: List[MarketTaker]):
        self.dex = dex
        self.marketTakers = marketTakers

    # This function calls transactions
    def run(self, numTransactions):
        actions = ['buyInsr', 'sellInsr']
        for i in range(numTransactions):
            action = random.choice(actions)
            actor = random.choice(self.marketTakers)
            print(actor)
            if action == 'buy':
                # if(self.__checksForBuyInsr()):
                pass
            elif action == 'sell':
                # print('sell!')
                pass
    
    def __checksForBuyInsr(self):
        pass