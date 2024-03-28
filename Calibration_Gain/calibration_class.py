import pymysql as ms
import uproot
import pandas as pd
from datetime import datetime
import math


class DatabaseConnector:
    def __init__(
        self, host="localhost", user="root", password="@Min08240707", database="test"
    ):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        self.connection = ms.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            charset="utf8mb4",
            cursorclass=ms.cursors.DictCursor,
        )

    def fetch_data(self, FEB, CH):
        try:
            with self.connection.cursor() as cursor:
                sql_query = (
                    "SELECT * FROM web_tt_calibration WHERE FEB_ID = %s and CH = %s"
                )
                cursor.execute(sql_query, (FEB, CH))
                rows = cursor.fetchall()
                df = pd.DataFrame(rows)
                df.to_csv("tt_calibration.csv", sep="\t", index=False)
                return df
        finally:
            self.connection.close()


class DataAnalyzer:
    @staticmethod
    def get_max_Q1(filepath):

        df = pd.read_csv(filepath, sep="\t")
        print(df)
        return df["Q_{1}"].max()

    @staticmethod
    def calculate_gain(charge):
        gain = charge * 1e-12 / (1.602e-19)
        return gain

    @staticmethod
    def ADC_to_charge(Q1, a1):
        return Q1 / a1


if __name__ == "__main__":
    db_connector = DatabaseConnector()
    db_connector.connect()
    data = db_connector.fetch_data(61, 47)
    print(data)
    a1 = data.loc[0, "a1"]
    filepath = "../Analysis_data/result_Final/CB22/ROB15/Final_result_CB22_ROB15.txt"
    Q1 = DataAnalyzer.get_max_Q1(filepath)
    charge = DataAnalyzer.ADC_to_charge(Q1, data.loc[0, "a1"])
    gain = DataAnalyzer.calculate_gain(charge)
    print(f"{a1}, {Q1}, {charge}, {gain:.2e}")
