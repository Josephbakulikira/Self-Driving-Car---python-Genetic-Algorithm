import math
import numpy as np

class ActivationFunction:
    def __init__(self, func, dfunc=None):
        self.func = func
        self.dfunc = dfunc

sigmoid = ActivationFunction(
    func = np.vectorize( lambda x : 1 / (1 + np.exp(-x)) ),
    dfunc = np.vectorize( lambda x: x * (1 - x) )
)

def stepFunction(val, step=0.5):
    if val < step:
        return 0
    else:
        return 1

tanh = ActivationFunction(
    func = np.vectorize( lambda x : np.tanh(x) ),
    dfunc = np.vectorize( lambda x : 1 - (x * x) )
)
