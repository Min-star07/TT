import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import erfc


def Linear_fc1(x, k):
    return k * x


def Linear_fc2(x, k, b):
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


def q_function(x, a00, a1, a2, a3, a4):
    if x < 2:
        return a1 * x
    else:
        index = -1 * a3 * np.power(x, a4)
        return a00 + a2 * (1 - np.exp(index))


def ADC_to_charge(Q1, a1):
    return Q1 / a1
