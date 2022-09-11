import numpy as np

def sigmoid(x):
  
        z = np.exp(-x)
        sig = 1 / (1 + z)
        return sig