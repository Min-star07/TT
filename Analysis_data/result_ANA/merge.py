import pandas as pd
import numpy as np
import os
import shutil
import sys
import time


def rename_folder_and_move_content(source_folder, destination_folder):
    # Check if the source folder exists
    if os.path.exists(source_folder):
        # If the destination folder already exists, rename it based on current time
        if os.path.exists(destination_folder):
            # Get current time to rename the folder
            current_time = time.strftime("%Y%m%d%H%M%S")
            renamed_folder = destination_folder + "_" + current_time
            os.rename(destination_folder, renamed_folder)
            print(f"Destination folder renamed to: {renamed_folder}")

        # Now move all files from source folder to destination folder
        # for file_name in os.listdir(source_folder):
        #     source_file = os.path.join(source_folder, file_name)
        #     destination_file = os.path.join(destination_folder, file_name)
        #     shutil.move(source_file, destination_file)
        #     print(f"Moved {source_file} to {destination_file}")
    else:
        print(f"Source folder {source_folder} does not exist.")


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
    print("CB : ", CB, "ROB:", ROB, "MODE:", MODE)
else:
    print("No arguments provided.")

# Destination folder path where you want to copy the figure
destination_folder = "../result_GEN/Result/CB" + str(CB) + "/ROB" + ROB
print(destination_folder)


# Read two files as DataFrames
outfilepath = "./Result/CB" + str(CB) + "/ROB" + str(ROB)
rename_folder_and_move_content(outfilepath, outfilepath)
outfilename = (
    "/CB" + str(CB) + "_ROB" + str(ROB) + "_final_result_mode_" + str(MODE) + ".txt"
)
# Destination folder creation (if not exist)
if not os.path.exists(outfilepath):
    os.makedirs(outfilepath)
    # shutil.rmtree(destination_folder)
    # print(f"Folder '{destination_folder}' deleted successfully.")
else:
    print(f"Directory '{outfilepath}' already exists.")
outfile = outfilepath + outfilename
# Check if the file exists and delete it if it does
if os.path.exists(outfile):
    os.remove(outfile)
    print(f"File {outfile} deleted successfully.")
else:
    print(f"File {outfile} does not exist.")

source_file = (
    destination_folder + "/fit_result_ROB_" + ROB + "_mode_" + str(MODE) + ".txt"
)
concatenated_df = pd.read_csv(source_file, sep="\t")
print(concatenated_df)
concatenated_df = concatenated_df.fillna(-1)
for i in range(64):
    # print(concatenated_df)
    data_select = concatenated_df[concatenated_df["Channel"] == i]
    # print(data_select)
    condition = (data_select["Sigma"] == 3) & (data_select["Chi2NDF"] < 3)
    if condition.any():
        data_channel_final = data_select[
            (data_select["Sigma"] == 3) & (data_select["Chi2NDF"] < 3)
        ]
        # sigma = data_channel_final.iloc[0, 5]
        # print(sigma)
        # copy_figure(ROB, i, sigma, source_folder, destination_folder)
        # Check if the file exists
        if not os.path.isfile(outfile):
            data_channel_final.to_csv(
                outfile, mode="a", header=True, index=False, sep="\t"
            )
        else:
            data_channel_final.to_csv(
                outfile, mode="a", header=False, index=False, sep="\t"
            )
    else:
        min_chi2overndf = data_select["Chi2NDF"].min()
        # print(f"=====find chi2 min===={min_chi2overndf}================================")
        # Remove duplicate rows based on specific columns (A and B in this case)
        unique_df = data_select.drop_duplicates(subset=["Chi2NDF"])
        data_channel_final = unique_df[(unique_df["Chi2NDF"] == min_chi2overndf)]
        # sigma = data_channel_final.iloc[0, 5]
        # copy_figure(ROB, i, sigma, source_folder, destination_folder)
        # Check if the file exists
        if not os.path.isfile(outfile):
            data_channel_final.to_csv(
                outfile, mode="a", header=True, index=False, sep="\t"
            )
        else:
            data_channel_final.to_csv(
                outfile, mode="a", header=False, index=False, sep="\t"
            )

# df = pd.read_csv(outfilename, sep="\t")
# print(df)
