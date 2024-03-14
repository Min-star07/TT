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
import pandas_ods_reader as ods

plt.style.use("mystyle.txt")


def hold_delay_test():
    filepath = "DT_20240129/holdtime.ods"
    df = ods.read_ods(filepath, 1)  # The second argument is the sheet index (0-based)
    print(df)
    ax = plt.axes(
        # xlim=[0, 250],
        ylim=[75, 100],
        xlabel="Hold delay",
        ylabel="charge [ADC]",
    )  # Adjust the layout to move the plot
    plt.errorbar(
        df["holddelay"],
        df["mean"] - 292,
        yerr=df["meanerror"],
        fmt=".",
        ecolor="red",
        capsize=7,
        # label="hold delay : 0-255",
    )
    # ax.xaxis.label.set_size(23)
    # ax.yaxis.label.set_size(23)
    # plt.axhline(y=292, color="red", linestyle=":")
    # plt.text(0.04, 0.15, "pedestal", transform=plt.gca().transAxes)
    # plt.legend()
    plt.savefig("holddelay_test1.pdf")
    plt.show()

    ax = plt.axes(
        xlim=[0, 255],
        # ylim=[75, 100],
        xlabel="Hold delay",
        ylabel="Hold time [ns]",
    )  # Adjust the layout to move the plot
    plt.scatter(
        df["holddelay"],
        df["t1"] - 39.36,
        label="hold delay time: fast or in -> hold",
    )
    print(df["t1"] - 39.36)
    plt.legend(loc=2, fontsize=12)
    # ax.xaxis.label.set_size(23)
    # ax.yaxis.label.set_size(23)
    plt.savefig("holddelay_test2.pdf")
    plt.show()
    filepath = "holddelay_test2.root"
    with uproot.create(filepath) as output_file:
        data = {"holddelay": df["holddelay"], "holdtime": df["t1"] - 39.36}
        output_file["tree"] = data

    ax = plt.axes(
        # xlim=[0, 250],
        # ylim=[290, 300],
        xlabel="Hold time [ns]",
        ylabel="Charge [ADC]",
    )  # Adjust the layout to move the plot
    plt.scatter(df["t1"] - 39.36, df["mean"] - 292)
    # ax.xaxis.label.set_size(23)
    # ax.yaxis.label.set_size(23)
    plt.savefig("holddelay_test3.pdf")
    plt.show()


def charge_vs_delta():
    # 1.0 p.e.
    filepath1 = "hold_charge1.txt"  # -100-150
    filepath2 = "hold_charge2.txt"  # -20, 40
    filepath3 = "hold_charge3.txt"  # -300, -200
    df1 = pd.read_csv(filepath1, sep="\t")
    df2 = pd.read_csv(filepath2, sep="\t")
    df3 = pd.read_csv(filepath3, sep="\t")
    df1 = df1.sort_values(by="hold time", ascending=False)
    df2 = df2.sort_values(by="hold time", ascending=False)
    df3 = df3.sort_values(by="hold time", ascending=False)
    print(df1)
    # dt1 = np.arange(-100, 155, 5)
    # dt2 = np.arange(-20, 41, 1)
    # dt3 = np.arange(-300, -90, 10)
    dt1 = np.arange(-150, 101, 5)
    dt2 = np.arange(-40, 21, 1)
    dt3 = np.arange(100, 301, 10)
    print(dt3)

    # 5 p.e.
    filepath4 = "hold_charge4.txt"
    filepath5 = "hold_charge5.txt"
    filepath6 = "hold_charge6.txt"
    df4 = pd.read_csv(filepath4, sep="\t")
    df5 = pd.read_csv(filepath5, sep="\t")
    df6 = pd.read_csv(filepath6, sep="\t")
    df4 = df4.sort_values(by="hold time", ascending=False)
    df5 = df5.sort_values(by="hold time", ascending=False)
    df6 = df6.sort_values(by="hold time", ascending=False)
    dt4 = np.arange(120, 402, 10)
    dt5 = np.arange(-70, 120, 10)
    dt6 = np.arange(-20, 21, 1)

    # 10p.e.
    filepath7 = "hold_charge7.txt"
    filepath8 = "hold_charge8.txt"
    filepath9 = "hold_charge9.txt"
    filepath10 = "hold_charge10.txt"  # -300, -200

    df7 = pd.read_csv(filepath7, sep="\t")
    df8 = pd.read_csv(filepath8, sep="\t")
    df9 = pd.read_csv(filepath9, sep="\t")
    df10 = pd.read_csv(filepath10, sep="\t")

    df7 = df7.sort_values(by="hold time", ascending=False)
    df8 = df8.sort_values(by="hold time", ascending=False)
    df9 = df9.sort_values(by="hold time", ascending=False)
    df10 = df10.sort_values(by="hold time", ascending=False)

    dt7 = np.arange(-100, 21, 20)
    dt8 = np.arange(-4, 11, 1)
    dt9 = np.arange(10, 301, 10)
    dt10 = np.arange(-30, -1, 1)

    filepath = "DT_20240129/holdtime.ods"
    df = ods.read_ods(filepath, 1)  # The second argument is the sheet index (0-based)

    ax = plt.axes(
        xlim=[-100, 300],
        # ylim=[0, 10],
        xlabel=r"T$_{tri}$ - T$_{sig}$ [ns]",
        ylabel="Charge [ADC]",
    )  # Adjust the layout to move the plot
    plt.axhline(y=297, linestyle=":", color="red")
    plt.text(-70, 265, "pedestal", c="red")

    # plt.axvline(x=20, linestyle="--", color="red")
    plt.axvline(x=0, linestyle=":", color="red")
    plt.scatter(
        dt1,
        df1["mean"],
        marker=".",
        c="green",
        label="1 p.e. , external hold delay, thre.:450",
    )
    plt.scatter(dt2, df2["mean"], marker=".", c="green")
    plt.scatter(dt3, df3["mean"], marker=".", c="green")
    plt.scatter(
        dt4,
        df4["mean"],
        marker=".",
        c="blue",
        label="5 p.e. , external hold delay, thre.:450",
    )
    plt.scatter(dt5, df5["mean"], marker=".", c="blue")
    plt.scatter(dt6, df6["mean"], marker=".", c="blue")
    print(max(df6["mean"]))
    max_index = df6["mean"].tolist().index(max(df6["mean"]))
    print(max_index)
    df6 = df6.reset_index()
    print(df6)
    print(df6.loc[max_index, "mean"])
    peak_location = max_index - 20
    plt.axvline(x=peak_location, linestyle=":", c="purple")
    plt.axvline(x=7, linestyle=":", c="purple")
    plt.text(-15, 600, "-5", c="purple")
    plt.text(10, 600, "7", c="purple")
    value_sub = [x - df.iloc[0, 3] for x in df2["mean"]]
    min_value = min(value_sub)
    min_index = value_sub.index(min_value)
    plt.scatter(
        dt7,
        df7["mean"],
        marker=".",
        c="black",
        label="10 p.e. , external hold delay, thre.:450",
    )
    plt.scatter(
        dt8,
        df8["mean"],
        marker=".",
        c="black",
        # label="10 p.e. , external hold delay, thre.:450",
    )
    plt.scatter(
        dt9,
        df9["mean"],
        marker=".",
        c="black",
        # label="10 p.e. , external hold delay, thre.:450",
    )
    plt.scatter(
        dt10,
        df10["mean"],
        marker=".",
        c="black",
        # label="10 p.e. , external hold delay, thre.:450",
    )
    specific_location_x = 7  # Example x-coordinate
    specific_location_y = df.iloc[0, 3]  # Example y-coordinate
    plt.scatter(
        specific_location_x,
        specific_location_y,
        color="red",
        marker="o",
        label="Charge @ hold delay = 0",
    )

    # plt.title("Hold delay = 0")
    plt.grid(which="both", alpha=0.2, linestyle=":")
    plt.legend(fontsize=12)
    plt.savefig("holddelay_test7.pdf")
    plt.show()


if __name__ == "__main__":
    # charge_vs_delta()
    hold_delay_test()
