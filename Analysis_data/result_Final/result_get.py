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
    result_corrected = filepath_current + "/check_channel.ods"
    # Check if the file exists
    if not os.path.exists(result_corrected):
        print(f"{result_corrected} is not exist, please confirm it----------")
        sys.exit()
    df = pd.read_excel(result_corrected, engine="odf")
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

    df_mode_final = []
    # modified result
    for i in df["Channel"].tolist():
        select_condition = df[df["Channel"] == i].iloc[0, 1]
        print(select_condition)
        filepath_mod = (
            "../result_Check/check/Result/fit_result_ROB_"
            + str(args.ROB)
            + "_channel_"
            + str(i)
            + ".txt"
        )
        df_mod = pd.read_csv(filepath_mod, sep="\t")
        print(df_mod)
        df_mode_result = df_mod[df_mod["Sigma"] == select_condition]
        print(df_mode_result)
        df_mode_final.append(df_mode_result)
    df_mode_final = pd.concat(df_mode_final)
    df_mode_final["log"] = 2
    print(df_mode_final)
    result = pd.concat([df_ori_select, df_mode_final])
    result = result.sort_values(by="Channel")
    result = result.reset_index(drop=True)
    print(result)
    result.to_csv(
        filepath_current
        + "/Final_result_CB"
        + str(args.CB)
        + "_ROB"
        + str(args.ROB)
        + ".txt",
        sep="\t",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analysis fit result")
    parser.add_argument("--CB", type=int, help="CB number", required=True)
    parser.add_argument("--ROB", type=int, help="ROB number", required=True)
    parser.add_argument("--mode", type=int, help="mode number", required=True)
    args = parser.parse_args()
    create_path(args)
    merge_result(args)
