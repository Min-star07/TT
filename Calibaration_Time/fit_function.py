import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import erfc


# def Linear_fc(x, k):
#     return k * x


def Linear_fc(x, k, b):
    return k * x + b


def concave_fc(x, a, b, c):
    return a * x * x + b * x + c


def exponential_fc(x, a, b, c):
    return a * np.exp(x, b) + c


def gauss_fc(x, a, b, c):
    return a * np.exp(-((x - b) ** 2) / (2 * c**2))


# Define a function using erfc
def erfc_fc(x, a, b, c):
    y = (x - b) / c
    return 0.5 * a * erfc(y / np.sqrt(2))
