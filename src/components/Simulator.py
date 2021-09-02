from .Dex import Dex
from .MarketTaker import MarketTaker
from typing import List
import random

# Parameters to set:
#   1. AMM parameters
#       a. Initial INSR reserve
#       b. Initial ETH reserve
#   2. MarketTaker parameters
#       a. Probabiliies for buy TKN, insure TKN, claim insurance, buy INSR, sell INSR?

# Note: Must handle exceptions from actors

# This class presets the behaviour of actors and handles interactions between them
class Simulator:
    def __init__(self, dex: Dex, marketTakers: List[MarketTaker]):
        self.dex = dex
        self.marketTakers = marketTakers

    # This function checks that ETH balance > 0 before INSR buys
    def __checksBeforeInsrBuy(self, actor: MarketTaker):
        return actor.ethBalance > 0

    # This function checks that INSR balance > 0 before INSR sells
    def __checksBeforeInsrSell(self, actor: MarketTaker):
        return actor.insrBalance > 0

    # This function processes all transactions in the simulation
    def run(self, numTransactions):
        actions = ['buyInsr', 'sellInsr']
        i = 0
        while i < numTransactions:
            actor = random.choice(self.marketTakers)
            # TODO: claim insurance for any active insured TKN with losses

            action = random.choice(actions)

            # Note: transactions that did not go through are not accounted for
            if action == 'buyInsr':
                if(self.__checksBeforeInsrBuy(actor)):
                    actor.buyInsr(self.dex)
                    i += 1
            elif action == 'sellInsr':
                if(self.__checksBeforeInsrSell(actor)):
                    actor.sellInsr(self.dex)
                    i += 1
