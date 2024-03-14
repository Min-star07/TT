import uproot
import pandas as pd
import argparse
import numpy as np


def read_calibration_result(args):
    print(f"The FEB number {args.FEB} and the CH number is {args.CH}")
    events = uproot.open("./test_b2.root:TB_lin_par")
    print(events.keys())
    print(events.show())
    data = events.arrays(
        [
            "FEB_ID",
            "cat_ID",
            "CH",
            "a0",
            "a00",
            "a1",
            "a2",
            "a3",
            "a4",
            "a5",
            "b",
            "ChiSq",
        ],
        library="pd",
    )  # library="np", library="pd"
    # data = data[(data["FEB_ID"] == args.FEB) ]
    data = data[(data["FEB_ID"] == args.FEB) & (data["CH"] == args.CH)]
    print(data)
    data.to_csv("cailibration_tt.txt", index=False, sep="\t")
    return data


def read_root_get_histogram(args):
    # Open the root file and get the histogram
    file = uproot.open("your_file.root")
    histogram = file["your_histogram"]

    # Get the histogram data
    bin_centers = histogram.axis().edges[:-1] + 0.5 * histogram.axis().binwidths
    bin_contents = histogram.values()

    # Calculate the mean and error
    mean = np.sum(bin_centers * bin_contents) / np.sum(bin_contents)
    error = np.sqrt(
        np.sum((bin_centers - mean) ** 2 * bin_contents) / np.sum(bin_contents)
    )

    print("Mean:", mean)
    print("Error:", error)
