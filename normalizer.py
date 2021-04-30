from math import exp

def normalize(score):
    """
    Normalize to get values between 0 and 1000.
    """
    return int(1 / (1 + exp(-score)) * 1000)
