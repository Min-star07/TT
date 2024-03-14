import pandas as pd
import numpy as np

filepath = "/home/lim/Desktop/TT/Program/Result_Final/check_channel.txt"
df = pd.read_csv(filepath, sep="\t")
print(df)

filepath1 = "/home/lim/Desktop/TT/Result/CB22/ROB15/CB22_ROB15_final_result_mode_2.txt"
df1 = pd.read_csv(filepath1, sep="\t")
df1_select = df1.drop(df["Channel"].tolist())
df1_select["log"] = 1
print(df1_select)


df2_select = []
filepath2 = "/home/lim/Desktop/TT/Program/result_Check1/Result/"
for i in df["Channel"].tolist():
    select_condation = df[df["Channel"] == i].iloc[0, 1]
    filepath3 = filepath2 + "fit_result_ROB_15_channel_" + str(i) + ".txt"
    df3 = pd.read_csv(filepath3, sep="\t")
    df3_select = df3[df3["Sigma"] == select_condation]
    df2_select.append(df3_select)
# Concatenate DataFrames along rows (axis=0)
df2_select = pd.concat(df2_select)
df2_select["log"] = 2
print(df2_select)
result = pd.concat([df1_select, df2_select])
result = result.sort_values(by="Channel")
result = result.reset_index(drop=True)
result.to_csv("test.txt", sep="\t")
