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


def calculate_charge(Av):
    exp = -Av / 20.0 + 1
    return pow(9.97, exp)


def error_calculate(eff):
    error_list = []
    for i in eff:
        efficiency = i / 100.0
        error = math.sqrt(efficiency * (1 - efficiency) / 1000.0)
        error_list.append(error)
    return error_list


filename = "effciency_vs_threshold.root"
if os.path.exists(filename):
    os.remove(filename)
    print(f"{filename} is deleted")
else:
    print(f"{filename} is not exist")
outrootfile = uproot.create(filename)
filepath = "DT_data_20240122/efficiency.xlsx"
sheetname = [
    0.1,
    0.2,
    0.3,
    0.4,
    0.5,
    0.6,
    0.7,
    0.8,
    0.9,
    1.0,
    1.2,
    1.4,
    1.6,
    1.8,
    2.0,
    2.2,
    2.5,
]

fig = plt.figure(figsize=(20, 10))
ax = plt.axes(
    xlim=[350, 1000],
    ylim=[0, 100],
    xlabel="DAC ",
    ylabel="efficiency [%]",
)  # Adjust the layout to move the plot
plt.subplots_adjust(left=0.08, right=0.9, top=0.9, bottom=0.1)
mu_list = []
for i in sheetname:
    treename = "photo_%s" % (str(i))
    df = pd.read_excel(filepath, sheet_name="%s" % (str(i)))
    df["Eff"] = df["Count"] / 1000 * 100
    error = error_calculate(df["Eff"])
    df["error"] = error
    outrootfile[treename] = df
    last_index = df["Eff"].tolist()[::-1].index(100)
    # Adjust the index to be relative to the original list
    last_index = len(df["Eff"]) - 1 - last_index
    first_index = df["Eff"].tolist()[::].index(0)
    sigma = df.iloc[first_index, 0] - df.iloc[last_index, 0]
    result = [i - 50 for i in df["Eff"]]
    min_value = min(result, key=abs)
    min_index = result.index(min_value)
    mu = df.iloc[min_index, 0]

    print(last_index, first_index, min_index, mu, sigma)
    popt, popv = curve_fit(fc.erfc_fc, df["DAC"], df["Eff"], p0=[100, mu, sigma])
    print(popt[0], popt[1], popt[2])
    fit_curve = fc.erfc_fc(df["DAC"], *popt)
    mu_list.append(popt[1])
    plt.text(popt[1] - 1, 52, "%d" % popt[1], color="C0")
    df.to_csv("DT_data_20240122/photo_%s.txt" % (str(i)), sep="\t", index=False)
    print(df)
    plt.errorbar(
        df["DAC"],
        df["Eff"],
        yerr=error,
        fmt="o",
        capsize=7,
        ecolor="black",
        label="thre : %s" % (str(i)),
    )
    plt.plot(
        df["DAC"],
        fit_curve,
        color="red",
        linewidth=2,
        # label="DAC : %d" % popt[1],
    )
outrootfile.close()
# Move the legend outside the plot area
plt.axhline(y=50, color="r", linestyle="--")
plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
plt.savefig("efficiency_vs_threshold1.pdf")
plt.show()
plt.close()


######################################################################################################################
popt, popv = curve_fit(fc.Linear_fc, sheetname, mu_list)
print(popt)
ax = plt.axes(
    # xlim=[350, 1050],
    # ylim=[0, 100],
    xlabel="threshold [p.e.]",
    ylabel="DAC",
)  # Adjust the layout to move the plot
plt.scatter(
    sheetname,
    mu_list,
    marker="o",
    label="DAC value @ effi. @ 50%",
)
x = np.array(sheetname)
y = fc.Linear_fc(x, *popt)
y_pe1_3 = fc.Linear_fc(1 / 3.0, *popt)
plt.plot(
    sheetname,
    y,
    linewidth=2,
    color="red",
    label="fit: DAC = %1.f * threshold + %1.f" % (popt[0], popt[1]),
)
plt.axhline(y=y_pe1_3, color="red", alpha=0.6, linestyle="--")
plt.axvline(x=1 / 3, color="red", alpha=0.6, linestyle="--")
plt.text(0.5, y_pe1_3, "%d @ 1/3 p.e." % (y_pe1_3))
plt.legend()
plt.savefig("efficiency_vs_threshold2.pdf")
plt.show()


ax = plt.axes(
    # xlim=[350, 1050],
    # ylim=[0, 100],
    xlabel="threshold [p.e.]",
    ylabel="DAC",
)  # Adjust the layout to move the plot
df = pd.read_csv("fitresult.txt", sep="\t")
print(df)
popt, popv = curve_fit(fc.Linear_fc, sheetname, df["mu"])
x = np.array(sheetname)
y = fc.Linear_fc(x, *popt)
y_pe1_3 = fc.Linear_fc(1 / 3.0, *popt)
plt.errorbar(
    sheetname,
    df["mu"],
    yerr=df["err1"],
    fmt="o",
    capsize=7,
    ecolor="black",
    label="DAC value @ effi. @ 50%",
)
plt.plot(
    sheetname,
    y,
    linewidth=2,
    color="red",
    label="fit: DAC = %1.f * threshold + %1.f" % (popt[0], popt[1]),
)
plt.legend()
plt.axhline(y=y_pe1_3, color="red", alpha=0.6, linestyle="--")
plt.axvline(x=1 / 3, color="red", alpha=0.6, linestyle="--")
plt.text(0.5, y_pe1_3, "%d @ 1/3 p.e." % (y_pe1_3))
plt.savefig("efficiency_vs_threshold2.pdf")
plt.show()
