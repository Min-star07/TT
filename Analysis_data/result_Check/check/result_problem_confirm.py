import pandas as pd
import os
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analysis fit result")
    parser.add_argument("--CB", type=int, help="CB number", required=True)
    parser.add_argument("--ROB", type=int, help="ROB number", required=True)
    parser.add_argument("--mode", type=int, help="mode number", required=True)
    args = parser.parse_args()

    filepath = (
        "../../result_Final/CB"
        + str(args.CB)
        + "/ROB"
        + str(args.ROB)
        + "check_channel.txt"
    )
    print(filepath)

    if os.path.exists(filepath):
        df = pd.read_csv(filepath, set="\t")
        print(df)
    else:
        print(f"{filepath} is not exit-----------------")
