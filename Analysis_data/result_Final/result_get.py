import argparse
import pandas as pd
import numpy as np
import os
import sys


def create_path(args):
    filepath = "./CB" + str(args.CB) + "/ROB" + str(args.ROB)
    print(filepath)
    if not os.path.exists(filepath):
        # os.removedirs(filepath)
        os.makedirs(filepath)
        print("folder is build, and deleted now, go on------")

    print(f"{filepath} is exit, please go on -----")


def merge_result(args):
    filepath_current = "./CB" + str(args.CB) + "/ROB" + str(args.ROB)
    print(filepath_current)
    result_corrected = filepath_current + "/check_channel.txt"
    # Check if the file exists
    if not os.path.exists(result_corrected):
        print(f"{result_corrected} is not exist, please confirm it----------")
        sys.exit()
    df = pd.read_csv(result_corrected, sep="\t")
    print(df)

    # origial result
    filepath_ori = (
        "../result_ANA/Result/CB"
        + str(args.CB)
        + "/ROB"
        + str(args.ROB)
        + "/CB"
        + str(args.CB)
        + "_ROB"
        + str(args.ROB)
        + "_final_result_mode_"
        + str(args.mode)
        + ".txt"
    )
    print(filepath_ori)
    df_ori = pd.read_csv(filepath_ori, sep="\t")
    print(df_ori)
    df_ori_select = df_ori.drop(df["Channel"].tolist())
    df_ori_select["log"] = 1
    print(df_ori_select)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analysis fit result")
    parser.add_argument("--CB", type=int, help="CB number", required=True)
    parser.add_argument("--ROB", type=int, help="ROB number", required=True)
    parser.add_argument("--mode", type=int, help="mode number", required=True)
    args = parser.parse_args()
    create_path(args)
    merge_result(args)
