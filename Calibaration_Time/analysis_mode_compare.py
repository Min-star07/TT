import uproot
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
from scipy.optimize import curve_fit
from matplotlib.backends.backend_pdf import PdfPages
import sys
import math
import os
import fit_function as fc

plt.style.use("mystyle.txt")

ax = plt.axes(
    xlabel="Charge injection [pC]",
    ylabel="Charge measured [ADC]",
)  # Adjust the layout to move the plot
charge_injection = [
    0.05,
    0.06,
    0.08,
    0.1,
    0.13,
    0.16,
    0.20,
    0.25,
    0.32,
    0.40,
    0.50,
    0.63,
    0.79,
    1,
    1.25,
    1.58,
    2.00,
    2.51,
    3.16,
    3.98,
    5.01,
    6.31,
    7.94,
    10,
]
print(charge_injection[::-1])
label = ["FADC", "Wilki"]
filename = ["charge_compare_FADC.txt", "charge_compare_wilki.txt"]
for i, item in enumerate(filename):
    df = pd.read_csv(item, sep="\t")
    print(df)
    if i == 0:
        charge_measure = df["chargemeasure"] / 10.0
    else:
        charge_measure = df["chargemeasure"]
    plt.errorbar(
        charge_injection[::-1],
        charge_measure,
        df["measureerror"],
        capsize=7,
        fmt=".",
        label=label[i],
    )
plt.legend()
plt.show()
