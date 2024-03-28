import pymysql as ms
import uproot
import pandas as pd
from datetime import datetime
import math


def connect_database(FEB, CH):
    # Establish connection parameters
    host = "localhost"  # Usually 'localhost' for local development
    user = "root"
    password = "@Min08240707"
    database = "test"

    # Create a connection object
    connection = ms.connect(
        host=host,
        user=user,
        password=password,
        db=database,
        charset="utf8mb4",
        cursorclass=ms.cursors.DictCursor,
    )

    try:
        # Use the connection to create a new table
        with connection.cursor() as cursor:
            # sql_query = """INSERT INTO tt_tele_fit_result(ROB, channel, fit_method, flag_chi2, Chi2NDF, ped_mean, ped_sigma, Sigma, Min_x, Max_x, N, Q0, Q1, sigma0, sigma1, w, alpha, mu) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            # sql_query = """INSERT INTO web_user(username, emailaddress, password, ctime, mtime) VALUES ('limin', 'limin@limin.niupi.com', '123456', '2023-12-19', '2023-12-19')"""
            # cursor.execute(sql_query)
            sql_query = (
                """SELECT * FROM web_tt_calibration WHERE FEB_ID = """
                + str(FEB)
                + """ and CH = """
                + str(CH)
            )
            # print(sql_query)
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            df = pd.DataFrame(rows)
            df.to_csv("tt_calibration.csv", sep="\t")
            for row in rows:
                # print(row)
                return row

    finally:
        # Close the connection
        connection.close()


def get_max_Q1():
    filepath = "../Analysis_data/result_Final/CB22/ROB15/Final_result_CB22_ROB15.txt"
    df = pd.read_csv(filepath, sep="\t")
    print(df)
    return df["Q_{1}"].max()


def calculate_gain(charge):
    gain = charge * 1e-12 / (1.602e-19)
    return gain


def ADC_to_charge(Q1, a1):
    return Q1 / a1


if __name__ == "__main__":
    result_calibration = connect_database(61, 47)
    print(result_calibration)
    a1 = result_calibration["a1"]
    print(a1)
    Q1 = get_max_Q1()
    print(Q1)
    charge = ADC_to_charge(Q1, a1)
    print(charge)
    gain = calculate_gain(charge)
    print(f"{gain:.2e}")
