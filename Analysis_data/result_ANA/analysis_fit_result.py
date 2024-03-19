import uproot
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
from scipy.optimize import curve_fit
from matplotlib.backends.backend_pdf import PdfPages
import sys

plt.style.use("mystyle.txt")


def fit_parameters_check(filepath, infile, CB, ROB, MODE):
    df = pd.read_csv(infile, sep="\t")
    print(df)
    figname = (
        filepath
        + "/CB"
        + str(CB)
        + "_ROB"
        + str(ROB)
        + "_final_parameters_mode_"
        + str(MODE)
        + ".pdf"
    )
    pdf_pages = PdfPages(figname)
    ax = plt.axes(
        xlim=[0, 63],
        # ylim=yrange,
        xlabel="Channel",
        ylabel=r"Q$_{0}$",
    )
    err = df["err2"].abs()
    plt.errorbar(
        df["Channel"],
        df["Q_{0}"],
        yerr=err,
        fmt=".",
        color="blue",
        capsize=7,
        ecolor="orangered",
        label=r"Q$_{0}$",
    )
    plt.title("CB" + str(CB) + "_ROB" + str(ROB) + r"_Q$_{0}$")
    plt.legend()
    pdf_pages.savefig()  # Save each figure to the PDF file
    plt.close()
    ###############################################################################################
    ax = plt.axes(
        xlim=[0, 63],
        # ylim=yrange,
        xlabel="Channel",
        ylabel=r"Q$_{1}$",
    )
    err = df["err3"].abs()
    plt.errorbar(
        df["Channel"],
        df["Q_{1}"],
        yerr=err,
        fmt=".",
        color="blue",
        capsize=7,
        ecolor="orangered",
        label=r"Q$_{1}$",
    )
    plt.title("CB" + str(CB) + "_ROB" + str(ROB) + r"_Q$_{1}$")
    plt.legend()
    pdf_pages.savefig()  # Save each figure to the PDF file
    plt.close()

    ##############################################################################################
    ax = plt.axes(
        xlim=[0, 63],
        # ylim=yrange,
        xlabel="Channel",
        ylabel=r"$\sigma_{0}$",
    )
    err = df["err4"].abs()
    plt.errorbar(
        df["Channel"],
        df["#sigma_{0}"],
        yerr=err,
        fmt=".",
        color="blue",
        capsize=7,
        ecolor="orangered",
        label=r"$\sigma_{0}$",
    )
    plt.title("CB" + str(CB) + "_ROB" + str(ROB) + r"_$\sigma_{0}$")
    plt.legend()
    pdf_pages.savefig()  # Save each figure to the PDF file
    plt.close()
    ###############################################################################################
    ax = plt.axes(
        xlim=[0, 63],
        # ylim=yrange,
        xlabel="Channel",
        ylabel=r"$\sigma_{1}$",
    )
    err = df["err5"].abs()
    plt.errorbar(
        df["Channel"],
        df["#sigma_{1}"],
        yerr=err,
        fmt=".",
        color="blue",
        capsize=7,
        ecolor="orangered",
        label=r"$\sigma_{1}$",
    )
    plt.title("CB" + str(CB) + "_ROB" + str(ROB) + r"_$\sigma_{1}$")
    plt.legend()
    pdf_pages.savefig()  # Save each figure to the PDF file
    plt.close()

    ###############################################################################################
    ax = plt.axes(
        xlim=[0, 63],
        # ylim=yrange,
        xlabel="Channel",
        ylabel=r"$w$",
    )
    err = df["err5"].abs()
    plt.errorbar(
        df["Channel"],
        df["w"],
        yerr=err,
        fmt=".",
        color="blue",
        capsize=7,
        ecolor="orangered",
        label=r"$w$",
    )
    plt.title("CB" + str(CB) + "_ROB" + str(ROB) + r"_$w$")
    plt.legend()
    pdf_pages.savefig()  # Save each figure to the PDF file
    plt.close()

    ###############################################################################################
    ax = plt.axes(
        xlim=[0, 63],
        # ylim=[0, 10],
        xlabel="Channel",
        ylabel=r"$\alpha$",
    )
    err = df["err5"].abs()
    plt.errorbar(
        df["Channel"],
        df["#alpha"],
        yerr=err,
        fmt=".",
        color="blue",
        capsize=7,
        ecolor="orangered",
        label=r"$\alpha$",
    )
    plt.title("CB" + str(CB) + "_ROB" + str(ROB) + r"_$\alpha$")
    plt.legend()
    pdf_pages.savefig()  # Save each figure to the PDF file
    plt.close()

    ###############################################################################################
    ax = plt.axes(
        xlim=[0, 63],
        xlabel="Channel",
        ylabel=r"$\mu$",
    )
    err = df["err5"].abs()
    plt.errorbar(
        df["Channel"],
        df["#mu"],
        yerr=err,
        fmt=".",
        color="blue",
        capsize=7,
        ecolor="orangered",
        label=r"$\mu$",
    )
    plt.title("CB" + str(CB) + "_ROB" + str(ROB) + r"_$\mu$")
    plt.legend()
    pdf_pages.savefig()  # Save each figure to the PDF file
    plt.close()

    ###############################################################################################
    pdf_pages.close()


def Data_check(infile, filepath):
    df = pd.read_csv(infile, sep="\t")
    # print(df)
    # df = df.iloc[:, 11:18]
    # print(df)
    # Select rows where any column has values less than 0
    df = df.drop(columns=["Sigma"])
    selected_data_negative = df[(df < 0).any(axis=1)]
    print(selected_data_negative)
    selected_data_sigma0 = df[(df["#sigma_{0}"] < 0) | (df["#sigma_{0}"] > 10)]
    selected_data_sigma1 = df[(df["#sigma_{1}"] < 0) | (df["#sigma_{1}"] > 100)]
    # print(selected_data_sigma0)
    # print(selected_data_sigma1)
    select_data = pd.concat(
        [selected_data_negative, selected_data_sigma0, selected_data_sigma1]
    )
    print(select_data)
    select_data["Channel"].to_csv(filepath + "/check_channel.txt", index=None)
    data_index = select_data.index
    index_list = data_index.tolist()
    print(index_list)
