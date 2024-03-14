import pandas as pd
import numpy as np
import sys


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
        MODE = sys.argv[3]
        print("CB:", CB, "ROB:", ROB, "MODE:", MODE)
    else:
        print("No arguments provided.")
    filepath = "./Result/CB" + str(CB) + "/ROB" + str(ROB)
    filename = (
        "/CB" + str(CB) + "_ROB" + str(ROB) + "_final_result_mode_" + str(MODE) + ".txt"
    )
    infile = filepath + filename
    Data_check(infile, filepath)
