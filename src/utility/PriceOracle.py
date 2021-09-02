import numpy as np

class PriceOracle:

    ethPrice = 3000.0

    # This function returns price of TKN, the volatile token to be insured in the simulation.
    # Price defined as a normal distribution with hard coded mean and variance
    @classmethod
    def getTknPrice(self):
        return np.random.normal(20, 2)