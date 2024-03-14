import pandas as pd
import numpy as np
import os
import shutil
import sys

def copy_figure(rob, channel, sigma, source_folder, destination_folder):
    # Figure name you want to copy
    figure_name = 'charge_rob' + str(rob) + '_channel_'+ str(channel) +'_sigma_'+ str(sigma) +'.pdf'  # Change this to your desired figure name
    # Source file path
    source_file_path = os.path.join(source_folder, figure_name)
    # Destination file path
    destination_file_path = os.path.join(destination_folder, figure_name)

    # Check if the file exists in the source folder
    if os.path.exists(source_file_path):
        # Copy the file to the destination folder
        shutil.copy(source_file_path, destination_folder)
        print(f"Figure '{figure_name}' copied successfully to {destination_folder}")
    else:
        print(f"File '{figure_name}' not found in the source folder: {source_folder}")

# Access command-line arguments
arguments = sys.argv
# Display command-line arguments
print("Number of arguments:", len(arguments))
print("Argument values:", arguments)
# Check if at least one argument was passed
if len(sys.argv) > 1:
    ROB = sys.argv[1]
    print("ROB:", ROB)
else:
    print("No arguments provided.")

# Source folder path where the figure is stored

# Destination folder path where you want to copy the figure
destination_folder = './Final_Result/'
# Destination folder creation (if not exist)
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)
    # shutil.rmtree(destination_folder)
    # print(f"Folder '{destination_folder}' deleted successfully.")
else:
    print(f"Directory '{destination_folder}' already exists.")

# Read two files as DataFrames
outfile = destination_folder + '/ROB_' + ROB + '_final_result.txt'
# Check if the file exists and delete it if it does
if os.path.exists(outfile ):
    os.remove(outfile )

concatenated_df = pd.read_csv('../Result/fit_result_ROB_' + ROB + '.txt', sep="\t")
print(concatenated_df)
for i in range(64):
    # print(concatenated_df)
    data_select = concatenated_df[concatenated_df["Channel"]==i]
    print(data_select)
    condition = (data_select["Sigma"] == 3) & (data_select["Chi2NDF"] < 3)
    if(condition.any()):
        data_channel_final = data_select[(data_select["Sigma"] == 3) & (data_select["Chi2NDF"] < 3)]
        # sigma = data_channel_final.iloc[0, 5]
        # print(sigma)
        # copy_figure(ROB, i, sigma, source_folder, destination_folder)
        # Check if the file exists
        if not os.path.isfile(outfile):
            data_channel_final.to_csv(outfile, mode="a", header=True, index=False, sep="\t")
        else:
            data_channel_final.to_csv(outfile, mode="a", header=False, index=False, sep="\t")
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
            data_channel_final.to_csv(outfile, mode="a", header=True, index=False, sep="\t")
        else:
            data_channel_final.to_csv(outfile, mode="a", header=False, index=False, sep="\t")



