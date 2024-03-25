import pymysql as ms
import uproot
import pandas as pd
from datetime import datetime

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
        # --------------------Example: Create a new database----------------------------
        # database_name = "CB22"
        # create_database_query = f"CREATE DATABASE {database_name}"
        # cursor.execute(create_database_query)
        # -----------------------Example: Drop databases---------------------------------
        # sql_query = "drop database CB22"
        # cursor.execute(sql_query)
        # --------------------Create a new table with columns---------------------------
        # sql_query = """CREATE TABLE IF NOT EXISTS TT_tele_calibration (id INT AUTO_INCREMENT PRIMARY KEY, FEB_ID INT, cat_ID INT, CH INT, a0 DOUBLE, a00 DOUBLE, a1 DOUBLE, a2 DOUBLE, a3 DOUBLE, a4 DOUBLE, a5 DOUBLE, b DOUBLE, ChiSq DOUBLE)"""
        # sql_query = """CREATE TABLE IF NOT EXISTS TT_tele_fit_result(id INT AUTO_INCREMENT PRIMARY KEY, ROB INT, channel INT, fit_method INT, flag_chi2 INT, Chi2NDF DOUBLE, ped_mean DOUBLE, ped_sigma DOUBLE, Sigma INT, Min_x DOUBLE,Max_x DOUBLE, N INT, Q0 DOUBLE, Q1 DOUBLE, sigma0 DOUBLE, sigma1 DOUBLE, w DOUBLE, alpha DOUBLE, mu DOUBLE)"""
        # sql_query = """CREATE TABLE IF NOT EXISTS CB22(id INT AUTO_INCREMENT PRIMARY KEY, ROB int not null, Channel int, flag_fit_method int, flag_chi2 int, Chi2NDF varchar(45), ped_mean varchar(45),ped_sigma varchar(45), Sigma int, Min_x varchar(45), Max_x varchar(45), N0 varchar(45), Q0 varchar(45), Q1 varchar(45), sigma0 varchar(45), sigma1 varchar(45), w varchar(45), alpha varchar(45), mu varchar(45), err1 varchar(45), err2 varchar(45), err3 varchar(45), err4 varchar(45), err5 varchar(45), err6 varchar(45), err7 varchar(45), err8 varchar(45), log int) default charset=utf8"""
        # cursor.execute(sql_query)
        ###delete table
        # sql_query = "drop table CB22"
        # sql_query = "delete from CB22"  ##only content
        # # # # sql_query = "truncate table tb_name"
        # cursor.execute(sql_query)
        # -------------------RENAME TABLE NAME--------------------------------------------
        # sql_query = '''rename table TT_tele_fit_result to tt_tele_fit_result'''
        # cursor.execute(sql_query)
        # --------------------------- add column------------------------------------------
        # sql_query = """alter table tb_name add col_name col_type DEFAULT value not null primary key"""
        # sql_query = """alter table CB22 add column Date timestamp default (curdate()) after id"""
        # sql_query = (
        #     """alter table CB22 add column Date date default '2024-03-01' after id"""
        # )
        # cursor.execute(sql_query)
        # -----------------------------delete column-------------------------------------
        # sql_query = """alter table CB22 drop column date"""
        # cursor.execute(sql_query)
        # -----------------------Modify column data type using ALTER TABLE
        # alter_query_type = "ALTER TABLE TTcalibration MODIFY COLUMN CH INT"
        # alter_query_type = "alter table tb_name change old_col_name new_col_name nuew type"
        # alter_query_type = """alter table tb_name alter col_name set default value"""
        # alter_query_type = """alter table tb_name alter col_name drop defalut"""
        # alter_query_type = """alter table tb_name add primary key (col_name)"""
        # alter_query_type = """alter table tb_name drop primary key"""
        # cursor.execute(alter_query_type)
        # ------------------------Rename column using ALTER TABLE
        # alter_query = "ALTER TABLE TTcalibration RENAME COLUMN data_ID TO CH"
        # cursor.execute(alter_query)
        # ------------------insert data-------------------------------------------------
        # sql_query = """INSERT INTO web_tt_calibration(FEB_ID, cat_ID, CH, a0, a00, a1, a2, a3, a4, a5, b, ChiSq) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        # sql_query = """INSERT INTO tt_tele_fit_result(ROB, channel, fit_method, flag_chi2, Chi2NDF, ped_mean, ped_sigma, Sigma, Min_x, Max_x, N, Q0, Q1, sigma0, sigma1, w, alpha, mu) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        # sql_query = """INSERT INTO web_user(username, emailaddress, password, ctime, mtime) VALUES ('limin', 'limin@limin.niupi.com', '123456', '2023-12-19', '2023-12-19')"""
        sql_query = """INSERT INTO CB22(ROB, Channel, flag_fit_method, flag_chi2, Chi2NDF, ped_mean, ped_sigma,  Sigma, Min_x, Max_x, N0, Q0, Q1, sigma0, sigma1, w, alpha, mu, err1, err2, err3, err4, err5, err6, err7, err8, log) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        # # cursor.execute(sql_query)
        df = pd.read_csv("./CB22/ROB15/Final_result_CB22_ROB15.txt", sep="\t")
        # df = df.iloc[:, 1:]
        # df = df.fillna(-1)
        print(df)

        for i in range(len(df["ROB"])):

            line = df.iloc[i, :]
            data = tuple(line)
            print(data)
            cursor.execute(sql_query, data)
        #####################################################################################################################################################################################
        # --------------------Execute a simple query------------------------------------
        # sql_query = "select * from CB22"
        # sql_query = "select * from CB22 where id  in (select id from web_user)"
        # sql_query = (
        #     "select * from CB22 where  exists (select id from CB22 where id in (1,4,6))"
        # )
        #
        # sql_query = (
        #     "select * from (select * from CB22 where id >60) as t where t.id > 62"
        # )

        ########################## join > on > where  > group by > having > order by > limit################################################################################################
        # sql_query = "select * from CB22 where id > '2_'"   %
        # sql_query = "select id, ROB, (SELECT MIN(id) from CB22) AS MIN_ID  from CB22"
        # sql_query = "select id, ROB, case when id < 9 then 'row1' else 'row3' end as rname from CB22"
        # sql_query = "select id, ROB, case when id < 9 then 'row1' else 'row3' end as rname from CB22"
        # sql_query = "select * from CB22 ORDER BY id DESC, Channel ASC"  # ASC
        # sql_query = "select * from CB22 order by id desc limit 10 "  # ASC
        # sql_query = "select * from CB22 order by id desc limit 10 offset 2"  # ASC
        # sql_query = "select Channel, count(id) from CB22 group by Channel having count(id) >= 1"  # ASC
        ##########################link table ##############################
        ## main table left outer join sub table on main taboe.x = sub table.x
        ## sub table right outer join main table on main taboe.x = sub table.x
        # sql_query = (
        #     """select * from CB22 left outer join web_user on CB22.id =  web_user.id"""
        # )
        # sql_query = (
        #     """select * from CB22 right outer join web_user on CB22.id =  web_user.id"""
        # )
        ## table inner join  table on  table.x = table.x
        # sql_query = (
        #     """select * from CB22 inner join web_user on CB22.id =  web_user.id"""
        # )
        # sql_query = """select id, Channel from CB22
        #     union all
        #     select id, Channel from CB22
        #     """
        ##constraint fk foreign key tb1(key) references tb(key)
        #################################user ###################################################################################################################################################
        # sql_query = """select Host, user from mysql.user"""
        ####create user 'username'@'ip' identified by 'password'
        ####grant all priviledges on *.* TO 'user'@'ip'         flush privileges

        # cursor.execute(sql_query)
        # result = cursor.fetchall()
        # for row in result:
        #     print(row)

    # Commit the changes
    connection.commit()

finally:
    # Close the connection
    connection.close()
