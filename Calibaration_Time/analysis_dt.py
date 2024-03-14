import uproot
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
from scipy.optimize import curve_fit
from matplotlib.backends.backend_pdf import PdfPages
import sys
import math
import pandas_ods_reader as ods
import os

plt.style.use("mystyle.txt")


def gaussian(x, a1, b1, c1):
    return a1 * np.exp(-((x - b1) ** 2) / (2 * c1**2))


def Save_to_rootfile(ifile, bin_edges, bin_values):
    # with uproot.create("output.root") as output_file:
    # Convert the histogram data to a TH1F (1D histogram) using uproot.fromnumpy()
    th1f_hist = np.histogram(
        bin_edges[:],
        bins=bin_edges,
        weights=bin_values,
    )
    print("=================")
    header, tail = os.path.split(ifile)
    print(header)
    print(tail)
    histoname = os.path.splitext(tail)[0]
    print(histoname)
    # Write the TH1F histogram to the ROOT file
    output_file[histoname] = th1f_hist


def Hist1D_Q1_distrubution(list_file):
    ax = plt.axes(
        # xlim=[25, 55],
        # ylim=[0, 150],
        xlabel="Delay time [ns]",
        ylabel="# of events",
    )
    try:
        for i, ifile in enumerate(list_file):
            print(i, ifile)
            df = pd.read_csv(
                ifile,
                sep=" ",
                skiprows=[0, 1, 2, 3],
            )
            print(df)
            print(df)
            bin_edges = df["Time"] * 1e9
            bin_values = df["Ampl"]
            time_mean = np.mean(bin_edges)
            time_std = np.std(bin_edges)
            print(time_mean, time_std)
            bin_centers = (bin_edges[:] + bin_edges[:]) / 2
            print(bin_centers)
            popt, pcov = curve_fit(
                gaussian, bin_centers, bin_values, p0=[40, time_mean, time_std]
            )
            print("Fitted parameters:", popt)

            plt.hist(
                bin_edges[:],
                bins=bin_edges,
                weights=bin_values,
                histtype="step",
                linewidth=2,
                label="Data : $mean = %.1f, std = %.1f$" % (time_mean, time_std),
            )
            plt.plot(
                bin_centers,
                gaussian(bin_centers, *popt),
                "r-",
                linewidth=2,
                label=r"fit : $\mu$ = %.1f, $\sigma$ = %.1f" % (popt[1], popt[2]),
            )
            plt.legend()
            # plt.show()

            Save_to_rootfile(ifile, bin_edges, bin_values)
    except:
        print("file" + str(i) + "is not exist")
    # Append the figure to the list
    pdf_pages.savefig()  # Save each figure to the PDF file
    plt.close()


def calculate_charge(Av):
    exp = -Av / 20.0 + 1
    return pow(10, exp) / 0.16


def error_calculate(err1, err2):
    print(err1[0])
    # err1 = err1.tolist()
    # err2 = err2.tolist()
    error_list = []
    for i in range(len(err2)):
        err = math.sqrt(pow(err1[i], 2) + pow(err2[i], 2))
        error_list.append(err)
    return error_list


def Graph2D_delaytime(filepath):
    # Read the ODS file into a pandas DataFrame
    df = ods.read_ods(filepath, 1)  # The second argument is the sheet index (0-based)
    df = df.sort_values(by="DB")
    output_file["dt"] = df
    print(df["DB"])
    charge_list = []
    for i, idb in enumerate(df["DB"]):
        charge = calculate_charge(idb)
        if idb == 46:
            print(charge)
            thre = charge
            dt1 = df.iloc[i, 6] - 14
            dt2 = df.iloc[i, 4] - 14
        charge_list.append(charge)
    # print(charge_list)
    ax = plt.axes(
        xlim=[0, 62],
        ylim=[4, 65],
        xlabel=r"p.e.",
        ylabel="mean delay time [ns]",
    )
    yerror2 = [0.01] * 28
    yerror1 = [0.01] * 28
    plt.errorbar(
        charge_list,
        df["mean2"] - 14,
        yerr=yerror2,
        marker=".",
        label="Fast or in",
    )
    plt.errorbar(
        charge_list,
        df["mean1"] - 14,
        yerr=yerror1,
        marker=".",
        label="Fast or out",
    )
    mean_dif = df["mean1"] - df["mean2"]
    # mean_err = error_calculate(df["std1"].tolist(), df["std2"].tolist())
    mean_err = error_calculate(yerror1, yerror2)
    plt.errorbar(
        charge_list,
        mean_dif,
        yerr=mean_err,
        marker=".",
        label="The differece of Fast or in and out ",
    )
    print(dt1, dt2)
    plt.axvline(x=thre, color="red", linestyle=":")
    plt.axhline(y=dt1, color="red", linestyle=":")
    plt.axhline(y=dt2, color="red", linestyle=":")
    plt.text(0.04, 0.6, "threshold = 1/3 p.e.", transform=plt.gca().transAxes)
    plt.grid(True, which="both", alpha=0.2, linestyle=":")
    plt.legend()
    plt.savefig("delay_time1.pdf")
    plt.show()
    ax = plt.axes(
        xlim=[8, 10],
        # ylim=[4, 65],
        ylabel="count",
        xlabel="The difference of in and out [ns]",
    )
    time_mean = np.mean(mean_dif)
    time_std = np.std(mean_dif)
    xrange = (8, 10)
    bin = 400
    plt.hist(
        mean_dif,
        bins=bin,
        range=xrange,
        histtype="step",
        linewidth=2,
        label="Data : $mean = %.1f, std = %.1f$" % (time_mean, time_std),
    )
    # popt, pcov = curve_fit(gaussian, mean_dif, 10, p0=[40, time_mean, time_std])
    # plt.plot(
    #     mean_dif,
    #     gaussian(mean_dif, *popt),
    #     "r-",
    #     linewidth=2,
    #     label=r"fit : $\mu$ = %.1f, $\sigma$ = %.1f" % (popt[1], popt[2]),
    # )
    # print("Fitted parameters:", popt)
    plt.legend()
    plt.savefig("diff.pdf")
    plt.show()


if __name__ == "__main__":
    # filepath = "./DT_data_20240122/F3--delaytimetest--00003.txt"
    # Output PDF file path
    list = [
        0,
        1,
        2,
        3,
        5,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
    ]

    filename = "delaytime_vs_photo.root"
    if os.path.exists(filename):
        os.remove(filename)
        print(f"{filename} is deleted")
    else:
        print(f"{filename} is not exist")
    with uproot.create(filename) as output_file:
        # tree = uproot.newtree(
        #     {
        #         "order": "int",
        #         "DB": "int",
        #         "charge": "double",
        #         "photo": "double",
        #         "mean1": "double"
        #         "std1" : "double",
        #         "mean2": "double"
        #         "std2" : "double",
        #     }
        # )

        pdf_pages = PdfPages("output.pdf")
        filepath = "./DT_data_20240122/delaytest/"
        for i in list:
            if i < 10:
                filepath_F2 = filepath + "F2--delaytimetest--0000" + str(i) + ".txt"
                filepath_F3 = filepath + "F3--delaytimetest--0000" + str(i) + ".txt"
            else:
                filepath_F2 = filepath + "F2--delaytimetest--000" + str(i) + ".txt"
                filepath_F3 = filepath + "F3--delaytimetest--000" + str(i) + ".txt"
            # print(filepath_F2, filepath_F3)
            list_file = [filepath_F2, filepath_F3]
            Hist1D_Q1_distrubution(list_file)
        pdf_pages.close()
        filepath = "./DT_data_20240122/result.ods"
        Graph2D_delaytime(filepath)
