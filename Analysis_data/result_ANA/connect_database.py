import pymysql as ms
import uproot
import pandas as pd
from datetime import datetime
# Establish connection parameters
host = 'localhost'  # Usually 'localhost' for local development
user = 'root'
password = '@Min08240707'
database = 'test'

# Create a connection object
connection = ms.connect(
    host=host,
    user=user,
    password=password,
    db=database,
    charset='utf8mb4',
    cursorclass=ms.cursors.DictCursor
)

try:
    # Use the connection to create a new table
    with connection.cursor() as cursor:
         # Example: Delete a record from the table
        # id_to_delete = 1  # Change this to the ID you want to delete
        # delete_query = "drop table telescope"
        # cursor.execute(delete_query)
        # delete_query = "TRUNCATE  TABLE TT_tele_calibration"
        # cursor.execute(delete_query)
        #--------------------Example: Create a new database----------------------------
        # database_name = 'new_database_name'
        # create_database_query = f"CREATE DATABASE {database_name}"
        #-------------------RENAME TABLE NAME---------------------------------
        # sql_query = '''rename table TT_tele_fit_result to tt_tele_fit_result'''
        # cursor.execute(sql_query)
        #--------------------Create a new table with columns---------------------------
        # sql_query = """CREATE TABLE IF NOT EXISTS TT_tele_calibration (id INT AUTO_INCREMENT PRIMARY KEY, FEB_ID INT, cat_ID INT, CH INT, a0 DOUBLE, a00 DOUBLE, a1 DOUBLE, a2 DOUBLE, a3 DOUBLE, a4 DOUBLE, a5 DOUBLE, b DOUBLE, ChiSq DOUBLE)"""
        # cursor.execute(sql_query)
        # sql_query = """CREATE TABLE IF NOT EXISTS TT_tele_fit_result(id INT AUTO_INCREMENT PRIMARY KEY, ROB INT, channel INT, fit_method INT, flag_chi2 INT, Chi2NDF DOUBLE, ped_mean DOUBLE, ped_sigma DOUBLE, Sigma INT, Min_x DOUBLE,Max_x DOUBLE, N INT, Q0 DOUBLE, Q1 DOUBLE, sigma0 DOUBLE, sigma1 DOUBLE, w DOUBLE, alpha DOUBLE, mu DOUBLE)"""
        
        # cursor.execute(sql_query)
        #------------------------Rename column using ALTER TABLE
        # alter_query = "ALTER TABLE TTcalibration RENAME COLUMN data_ID TO CH"
        # cursor.execute(alter_query)
        #-----------------------Modify column data type using ALTER TABLE
        # alter_query_type = "ALTER TABLE TTcalibration MODIFY COLUMN CH INT"
        # cursor.execute(alter_query_type)
        #--------------------Execute a simple query------------------------------------
        # sql_query = "SELECT * FROM TTcalibration"
        # cursor.execute(sql_query)
        # result = cursor.fetchall()
        # for row in result:
        #     print(row)
        
        #------------------insert data-------------------------------------------------
        # sql_query = """INSERT INTO web_tt_calibration(FEB_ID, cat_ID, CH, a0, a00, a1, a2, a3, a4, a5, b, ChiSq) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        sql_query = """INSERT INTO tt_tele_fit_result(ROB, channel, fit_method, flag_chi2, Chi2NDF, ped_mean, ped_sigma, Sigma, Min_x, Max_x, N, Q0, Q1, sigma0, sigma1, w, alpha, mu) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        # sql_query = """INSERT INTO web_user(username, emailaddress, password, ctime, mtime) VALUES ('limin', 'limin@limin.niupi.com', '123456', '2023-12-19', '2023-12-19')"""
        # cursor.execute(sql_query)
        df = pd.read_csv("./Final_Result_test/ROB_15_final_result.txt", sep="\t")

        for i in range(len(df["ROB"])):
           line = df.iloc[i, :]
           data = tuple(line)
           print(data)
           cursor.execute(sql_query, data)
       
    # Commit the changes
    connection.commit()

finally:
    # Close the connection
    connection.close()
