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

    # This function processes all transactions in the simulation
    def run(self, numTransactions):
        actions = ['buyInsr', 'sellInsr']
        for i in range(numTransactions):
            action = random.choice(actions)
            actor = random.choice(self.marketTakers)
            if action == 'buyInsr':
                if(self.__checksForBuyInsr(actor)):
                    actor.buyInsr(self.dex)
            elif action == 'sellInsr':
                print('sell!')
    
    def __checksForBuyInsr(self, actor: MarketTaker):
        return actor.ethBalance > 0