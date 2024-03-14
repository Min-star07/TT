import uproot
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
from scipy.optimize import curve_fit
import math
import sys

plt.style.use("mystyle.txt")


def cacaulate_error(list_Q1, list_Q1_error, p):
    error = []
    for i in range(len(list_Q1[0])):
        x = list_Q1[0][i]
        y = list_Q1[0][i]
        x_error = list_Q1_error[0][i]
        y_error = list_Q1_error[1][i]
        # print(i, x, y, x_error, y_error)
        y1 = -(x / (y * y))
        f1 = pow(1.0 / y, 2) * pow(x_error, 2) + pow(y1, 2) * pow(y_error, 2)
        f2 = 2 * 1.0 / y * y1 * p * x_error * y_error
        # print(f1 + f2)
        err = math.sqrt(f1 + f2)
        error.append(err)
    return error


# Define the double Gaussian function
def gaussian(x, a1, b1, c1):
    return a1 * np.exp(-((x - b1) ** 2) / (2 * c1**2))


def Hist1D_Q1_ratio(list_Q1, list_Q1_error):
    covariance_matrix = np.cov(list_Q1[0], list_Q1[1])
    # Extract covariance between x and y (element at position (0, 1) or (1, 0))
    cov_xy = covariance_matrix[0, 1]

    print("Covariance matrix:")
    print(covariance_matrix)
    print(f"Covariance between x and y: {cov_xy}")

    correlation_coefficient = np.corrcoef(list_Q1[0], list_Q1[1])[0, 1]
    print(f"Correlation coefficient between x and y: {correlation_coefficient}")

    error = cacaulate_error(list_Q1, list_Q1_error, correlation_coefficient)
    # print(error)

    # Using list comprehension to divide elements

    result = [y / x for x, y in zip(list_Q1[0], list_Q1[1])]
    # Q1 diatrubution
    # Create an error plot
    ax = plt.axes(
        xlim=[0, 63],
        ylim=[6, 16],
        xlabel="Channel",
        ylabel="FADC / WilKi ADC",
    )  # r"$\\frac{{\\chi^2}}{{\\text{{NDF}}}}"
    plt.errorbar(
        df["Channel"],
        result,
        yerr=error,
        fmt=".",
        color="blue",
        capsize=7,
        ecolor="orangered",
    )

    # Add legend
    plt.title("CB" + str(CB) + "_ROB" + str(ROB) + "_FADC/Wilki ADC")
    figname = filepath + "/CB" + str(CB) + "_ROB" + str(ROB) + "_final_Q1_Ratio1.pdf"
    plt.savefig(figname)
    # Show the plot
    plt.show()

    ##################################################################################################################################
    y_mean = np.mean(result)

    y_std = np.std(result)
    xrange = (0, 20)
    bins = 100
    # Create a histogram from the data
    hist, bin_edges = np.histogram(result, range=xrange, bins=bins, density=False)
    # print(hist)
    # print(bin_edges)

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

    ax = plt.axes(
        xlim=[4, 20],
        ylim=[0, 16],
        xlabel=r"FADC / Wilkinson ADC ",
        ylabel="# of events [/0.2]",
    )  # r"$\\frac{{\\chi^2}}{{\\text{{NDF}}}}"
    plt.hist(
        result,
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
    # plt.text(0.6, 0.6, 'Relative Text', fontsize=12, color='blue', transform=plt.gca().transAxes)

    # Add legend
    plt.title("CB" + str(CB) + "_ROB" + str(ROB) + "_FADC/Wilki ADC")
    plt.legend()
    figname = filepath + "/CB" + str(CB) + "_ROB" + str(ROB) + "_final_Q1_Ratio2.pdf"
    plt.savefig(figname)
    plt.show()


def Hist2D_Q1_ratio(list_Q1):
    result = [y / x for x, y in list(zip(list_Q1[0], list_Q1[1]))]
    plt.figure(figsize=(9, 9))
    # Reshape the list into an 8x8 array
    print(len(result))
    array_8x8 = np.array(result).reshape(8, 8)
    data = array_8x8
    # Create a 8x8 grid plot with colored cells representing values
    plt.imshow(data, cmap="viridis", interpolation="nearest")
    # Add text annotations for each cell
    for i in range(8):
        for j in range(8):
            plt.text(j, i, f"{data[i, j]:.1f}", ha="center", va="center", color="white")

    # Set colorbar to represent values
    # plt.colorbar(label=r"")

    # Set labels and title
    plt.xlabel("Channel")
    plt.ylabel("Channel")
    # Add legend
    plt.title("CB" + str(CB) + "_ROB" + str(ROB) + "_Q1_FADC/Wilki ADC")
    figname = filepath + "/CB" + str(CB) + "_ROB" + str(ROB) + "_final_Q1_Ratio3.pdf"
    plt.savefig(figname)
    plt.show()


if __name__ == "__main__":
    # Access command-line arguments
    arguments = sys.argv
    # Display command-line arguments
    print("Number of arguments:", len(arguments))
    print("Argument values:", arguments)
    # Check if at least one argument was passed
    if len(sys.argv) > 1:
        CB = sys.argv[1]
        ROB = sys.argv[2]
        file1 = sys.argv[3]
        file2 = sys.argv[4]
        print("CB:", CB, "ROB", ROB, "file1:", file1, "file2:", file2)

    else:
        print("No arguments provided.")
    list_filepath = [file1, file2]
    list_Q1 = []
    list_Q1_error = []
    filepath = "../../Result/CB" + str(CB) + "/ROB" + str(ROB)
    for i in list_filepath:
        infile = filepath + i
        df = pd.read_csv(infile, sep="\t")
        print(df)
        list_Q1.append(df["Q_{1}"].tolist())
        list_Q1_error.append(df["err3"].abs().tolist())
    print(len(list_Q1[0]))
    Hist1D_Q1_ratio(list_Q1, list_Q1_error)
    Hist2D_Q1_ratio(list_Q1)
