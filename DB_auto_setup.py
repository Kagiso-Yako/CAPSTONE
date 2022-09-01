import sqlite3
import wget
import urllib.request as rq
import pandas as pd

from SQL_queries import SQL_queries


class DB_auto_setup:
    def __init__(self, DB_name):
        self.DB_name = DB_name

    @staticmethod
    def excel_to_csv(filepath, columns=None):
        data_xls = pd.read_excel(filepath, 'Current Rated Researchers (Webs', dtype=str, index_col=None)
        if columns is not None:
            data_xls.columns = columns

        data_xls.to_csv('DB.csv', encoding='utf-8', index=False, header=True)

    @staticmethod
    def csv_to_db(csv_file, table_name, columns, DB_name, primary_key=None):
        conn = sqlite3.connect(DB_name)
        conn.execute(SQL_queries.delete_table(table_name))

        df = pd.read_csv(csv_file)
        conn.execute(SQL_queries.create_table(table_name, columns, primary_key))

        df.to_sql(table_name, conn, if_exists="append", index=False)

    @staticmethod
    def download_from_url(url):
        wget.download(url, "c:/users/Mthulisi/downloads/CAPSTONE/CAPSTONE/test")
        data = rq.urlopen(url)
        print(data.headers['Last-Modified'])
