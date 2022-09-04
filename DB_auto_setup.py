import sqlite3
import wget
import requests
import urllib.request as rq
import pandas as pd
from threading import Thread
from time import sleep
from datetime import date
import calendar

from SQL_queries import SQL_queries


class DB_auto_setup:
    def __init__(self, DB_name, NRF_Excel_path, excel_sheet_name, columns_csv, csv_file, table_name, table_columns,
                 url):
        requests.packages.urllib3.disable_warnings()
        self.DB_name = DB_name
        self.NRF_Excel_path = NRF_Excel_path
        self.excel_sheet_name = excel_sheet_name
        self.columns_csv = columns_csv
        self.csv_file = csv_file
        self.table_name = table_name
        self.table_columns = table_columns
        self.url = url
        # Default date modified
        self.last_modified = "Mon, 22 Aug 2022 07:57:10 GMT"
        self.set_last_modified()

        check_date = Thread(target=self.update)
        check_date.start()

    @staticmethod
    def excel_to_csv(filepath, sheet, columns=None):
        # convert excel data
        data_xls = pd.read_excel(filepath, sheet, dtype=str, index_col=None)
        if columns is not None:
            data_xls.columns = columns

        data_xls.to_csv('DB.csv', encoding='utf-8', index=False, header=True)

    def csv_to_db(self, csv_file, table_name, columns):
        # Creating a connection to the database
        conn = sqlite3.connect(self.DB_name)

        # Deleting the old table to replace with a new one
        conn.execute(SQL_queries.delete_table(table_name))

        # Reading csv file, then creating an empty table and appending the csv file data to it
        df = pd.read_csv(csv_file)
        conn.execute(SQL_queries.create_table(table_name, columns))
        df.to_sql(table_name, conn, if_exists="append", index=False)

    def download_from_url(self):
        try:
            # Download file then save to Data folder, then check if it has changed
            wget.download(self.url, "c:/users/Mthulisi/downloads/CAPSTONE/CAPSTONE/Data")

        except requests.exceptions.RequestException as e:
            print(e.request + "Could not find the file")

    def update(self):
        while True:
            # Check if the file on the sever is outdated, if not download and convert to DB format.
            # This will repeat every 1 min.
            self.url = self.build_url()
            try:
                # somewhere write to file to save the date permanently
                if requests.head(self.url, verify=False).status_code == 200:
                    data = rq.urlopen(self.url)
                    if data.headers['last-modified'] != "Mon, 22 Aug 2022 07:57:10 GMT":
                        self.download_from_url()
                        self.excel_to_csv(self.NRF_Excel_path, self.excel_sheet_name, self.columns_csv)
                        self.csv_to_db(self.csv_file, self.table_name, self.table_columns)
            except requests.exceptions.RequestException as e:
                print(e.request + "Could not find the file")
            sleep(450)

    @staticmethod
    def build_url():
        # Build url based on the NRF url format
        month_num = '{:02d}'.format(date.today().month)
        year_num = str(date.today().year)
        month_name = calendar.month_name[date.today().month]
        day_num = '{:02d}'.format(date.today().day)

        url = "https://www.nrf.ac.za/wp-content/uploads/" + \
              year_num + "/" + month_num + "/Current-Rated-Researchers-" + \
              day_num + "-" + month_name + "-" + year_num + ".xlsx"
        return url

    def set_last_modified(self):
        try:
            with open("Data/Last_modified.txt") as filestream:
                self.last_modified = filestream.readline()
        except:
            print("Unable to open file!")
