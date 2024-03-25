import uproot
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
from scipy.optimize import curve_fit
from matplotlib.backends.backend_pdf import PdfPages
import sys

# from analysis_fit_result import fit_parameters_check

plt.style.use("mystyle.txt")


def Calculate_chi2ndf(filepath, infile, CB, ROB, MODE):
    df = pd.read_csv(infile, sep="\t")
    print(df)
    y_max = np.max(df["Q_{1}"])
    y_min = np.min(df["Q_{1}"])
    y_mean = np.mean(df["Q_{1}"])
    y_std = np.std(df["Q_{1}"])

    if MODE == 1:
        yrange = [0, 16]
    else:
        yrange = [0, 160]
    err = df["err1"]
    print(yrange)
    ax = plt.axes(xlim=[0, 63], ylim=yrange, xlabel="Channel", ylabel=r"Q$_{1}$")
    plt.scatter(
        df["Channel"],
        df["Chi2NDF"],
        marker="*",
        c="red",
        alpha=0.5,
        label=r"$\frac{\chi^2}{NDF}$",
    )  # Plotting the histogram
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
    if MODE == 1:
        plt.fill_between(
            x=df["Channel"],
            y1=y_min,
            y2=y_max,
            color="pink",
            interpolate=True,
            alpha=0.2,
        )
        plt.text(
            0.4,
            0.9,
            "mean = %.1f" % (y_mean),
            color="red",
            transform=plt.gca().transAxes,
        )
        plt.text(
            0.4, 0.8, "max = %.1f" % (y_max), color="C0", transform=plt.gca().transAxes
        )
        plt.text(
            0.4, 0.7, "min = %.1f" % (y_min), color="C0", transform=plt.gca().transAxes
        )
        plt.text(14, 5, "y=3", color="blue")
    if MODE == 2:
        plt.fill_between(
            x=df["Channel"],
            y1=y_min,
            y2=y_max,
            color="pink",
            interpolate=True,
            alpha=0.2,
        )
        plt.text(
            0.4,
            0.4,
            "mean = %.1f" % (y_mean),
            color="red",
            transform=plt.gca().transAxes,
        )
        plt.text(
            0.4, 0.3, "max = %.1f" % (y_max), color="C0", transform=plt.gca().transAxes
        )
        plt.text(
            0.4, 0.2, "min = %.1f" % (y_min), color="C0", transform=plt.gca().transAxes
        )
        plt.text(14, 6, "y=3", color="blue")
    plt.axhline(y=y_min, color="C0", linestyle="--")  # Horizontal line at y_min
    plt.axhline(y=y_mean, color="red", linestyle="--")  # Horizontal line at y_max
    plt.axhline(y=y_max, color="C0", linestyle="--")  # Horizontal line at y_max
    plt.axhline(y=3, color="blue", linestyle="--")  # Horizontal line at y_max
    # plt.axvline(x=2, color='green', linestyle='-.', linewidth=2)  # Vertical line at x=2
    plt.title("CB" + str(CB) + "_ROB" + str(ROB))
    plt.legend()
    figname = (
        filepath
        + "/CB"
        + str(CB)
        + "_ROB"
        + str(ROB)
        + "_final_Q1_mode_"
        + str(MODE)
        + "_1.pdf"
    )
    plt.savefig(figname)
    plt.show()


# Define the double Gaussian function
def gaussian(x, a1, b1, c1):
    return a1 * np.exp(-((x - b1) ** 2) / (2 * c1**2))


def Hist1D_Q1_distrubution(filepath, infile, CB, ROB, MODE):
    df = pd.read_csv(infile, sep="\t")
    print(df)
    y_mean = np.mean(df["Q_{1}"])
    y_std = np.std(df["Q_{1}"])
    print(MODE)
    if MODE == 1:
        xrange = [4, 16]
        bins = 120
    else:
        xrange = [40, 160]
        bins = 120
    # Create a histogram from the data
    hist, bin_edges = np.histogram(df["Q_{1}"], range=xrange, bins=bins, density=False)
    print(hist)
    print(bin_edges)

    # Get the bin centers
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    # Fit the histogram data to the double Gaussian function
    popt, pcov = curve_fit(gaussian, bin_centers, hist, p0=[40, y_mean, y_std])
    print("Fitted parameters:", popt)
    # Get observed data (bin contents) from the histogram
    observed_data = hist  # Replace this with your actual histogram data
    # Calculate expected values using the fitted model
    expected_data = gaussian(
        bin_centers, popt[0], popt[1], popt[2]
    )  # Replace bin_centers with your bin centers

    # Calculate chi-squared
    residuals = observed_data - expected_data
    chi_squared = np.sum(residuals**2)

    # Calculate degrees of freedom
    num_params = 3
    num_bins = len(observed_data)
    ndf = num_bins - num_params

    # Calculate chi-squared per degree of freedom
    chi_squared_ndf = chi_squared / ndf

    print(f"Chi-squared: {chi_squared}")
    print(f"Degrees of freedom: {ndf}")
    print(f"Chi-squared per degree of freedom: {chi_squared_ndf}")

    ax = plt.axes(xlim=xrange, ylim=[0, 10], xlabel=r"Q$_{1}$", ylabel="# of events")
    plt.hist(
        df["Q_{1}"],
        range=xrange,
        bins=bins,
        label="Q$_{1}$: mean = %.1f, std = %.1f" % (y_mean, y_std),
    )
    plt.plot(
        bin_centers,
        gaussian(bin_centers, *popt),
        "r-",
        linewidth=2,
        label=r"fit : $\mu$ = %.1f, $\sigma$ = %.1f" % (popt[1], popt[2]),
    )  # Plotting the fitted curve

    # Add text at a relative position (using relative coordinates)
    plt.title("CB" + str(CB) + "_ROB" + str(ROB))
    plt.legend()
    figname = (
        filepath
        + "/CB"
        + str(CB)
        + "_ROB"
        + str(ROB)
        + "_final_Q1_mode_"
        + str(MODE)
        + "_2.pdf"
    )
    plt.savefig(figname)
    plt.show()


def Hist2D_Q1_distrubution(filepath, infile, CB, ROB, MODE):
    df = pd.read_csv(infile, sep="\t")
    print(df)
    # Generate sample data for a 8x8 grid (replace this with your data)
    numbers = list(df["Q_{1}"])
    print(numbers)
    # Reshape the list into an 8x8 array
    array_8x8 = np.array(numbers).reshape(8, 8)
    data = array_8x8
    # Create a 8x8 grid plot with colored cells representing values
    plt.figure(figsize=(10, 10))
    plt.imshow(data, cmap="viridis", interpolation="nearest")
    # Add text annotations for each cell
    for i in range(8):
        for j in range(8):
            plt.text(j, i, f"{data[i, j]:.1f}", ha="center", va="center", color="white")
    # Set colorbar to represent values
    # plt.colorbar(label=r"Q$_{1}$ value")
    # Set labels and title
    plt.xlabel("Channel")
    plt.ylabel("Channel")
    plt.title("CB" + str(CB) + "_ROB" + str(ROB) + "_FADC")
    figname = (
        filepath
        + "/CB"
        + str(CB)
        + "_ROB"
        + str(ROB)
        + "_final_Q1_mode_"
        + str(MODE)
        + "_3.pdf"
    )
    plt.savefig(figname)
    plt.show()


# if __name__ == "__main__":
#     # Access command-line arguments
#     arguments = sys.argv
#     # Display command-line arguments
#     print("Number of arguments:", len(arguments))
#     print("Argument values:", arguments)
#     # Check if at least one argument was passed
#     if len(sys.argv) > 1:
#         CB = sys.argv[1]
#         ROB = sys.argv[2]
#         MODE = sys.argv[3]
#         print("CB:", CB, "ROB:", ROB, "MODE:", MODE)
#     else:
#         print("No arguments provided.")
#     filepath = "./Result/CB" + str(CB) + "/ROB" + str(ROB)

#     filename = (
#         "/CB" + str(CB) + "_ROB" + str(ROB) + "_final_result_mode_" + str(MODE) + ".txt"
#     )
#     infile = filepath + filename
#     MODE = int(MODE)
#     fit_parameters_check(filepath, infile, CB, ROB, MODE)
#     Calculate_chi2ndf(infile, CB, ROB, MODE)
#     Hist1D_Q1_distrubution(infile, CB, ROB, MODE)
#     Hist2D_Q1_distrubution(infile, CB, ROB, MODE)
