#AI researchers are based at South Africa’s
#26 public universities and other research-based organisations. They publish the results of their research in
#a variety of venues, including journals, conference proceedings and workshop proceedings. The
#application will draw from and consolidate data from multiple public research data sources, including the
#researcher rating system used by the National Research Foundation (NRF) and Microsoft Academic
#Graph (MAG). A web based interface must be provided for users to perform queries and visualise
#information about the research community including: a) dominant research areas/topics, publications
#venues, collaborations (co-authors) and impact (citations) (b) t++in which
#researchers are based (c) finding interesting trends and patterns over time, (c) appropriate metrics to
#assess and analyse the community and network structure, and (d) manual update and synchronisation
#functionality with MAG, the NRF and other public data sources.
import sqlite3

from flask import Flask, render_template

from DB_auto_setup import DB_auto_setup

# Global variables
# Defines the columns for the csv file and the columns for the NRF researchers table
from DB_manager import DB_manager
from SQL_queries import SQL_queries

table_name = "Researchers"
NRF_Excel_path = "Data/Current-Rated-Researchers-22-August-2022.xlsx"
excel_sheet_name = 'Current Rated Researchers (Webs'
csv_file = "Data/DB.csv"
NRF_database_file = "Data/Database.db"
url = "https://www.nrf.ac.za/wp-content/uploads/2022/08/Current-Rated-Researchers-22-August-2022.xlsx"

columns = ["id INTEGER primary key autoincrement",
           "Surname TEXT",
           "Initials TEXT",
           "Title TEXT",
           "Institution TEXT",
           "Rating TEXT",
           "Rating_Start DATE",
           "Rating_Ending DATE",
           "PrimaryResearch TEXT",
           "SecondaryResearch TEXT",
           "Specializations TEXT"]

columns_csv = ["Surname",
               "Initials",
               "Title",
               "Institution",
               "Rating",
               "Rating_Start",
               "Rating_Ending",
               "PrimaryResearch",
               "SecondaryResearch",
               "Specializations"]

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/researchers")
def researchers():
    rows = None
    S_options = None
    P_options = None
    Institutions = None
    Surnames = None

    try:
        conn = sqlite3.connect(NRF_database_file)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        try:
            cursor.execute(SQL_queries.get_table(table_name))
            rows = cursor.fetchall()
        except sqlite3.Error:
            print("Unable to obtain rows")

        try:
            cursor.execute(SQL_queries.get_table(table_name, single_column="SecondaryResearch", DISTINCT=True))
            S_options = cursor.fetchall()
        except sqlite3.Error:
            print("Unable to obtain secondary research options")
        try:
            cursor.execute(SQL_queries.get_table(table_name, single_column="PrimaryResearch", DISTINCT=True))
            P_options = cursor.fetchall()
        except sqlite3.Error:
            print("Unable to obtain primary research options")
        try:
            cursor.execute(SQL_queries.get_table(table_name, single_column="Institution", DISTINCT=True))
            Institutions = cursor.fetchall()
        except sqlite3.Error:
            print("Unable to obtain Institutions")
        try:
            cursor.execute(SQL_queries.get_table(table_name, single_column="Surname", DISTINCT=True))
            Surnames = cursor.fetchall()
        except sqlite3.Error:
            print("Unable to obtain Surnames")

    except sqlite3.Error:
        print("Could not connect to database!")

    return render_template("researchers.html", rows=rows, S_options=S_options, P_options=P_options,
                           Institutions=Institutions, Surnames=Surnames)


@app.route("/trendsAndAnalysis")
def trendsAndAnalysis():
    return render_template("TrendsAndAnalysis.html")

@app.route("/institutions")
def institutions():
    return render_template("institutions.html")

@app.route("/universityofcpt")
def universityofcpt():
    return render_template("institution.html")

if __name__ == '__main__':
    table = "Researchers"
    auto = DB_auto_setup(NRF_database_file, NRF_Excel_path, excel_sheet_name, columns_csv, csv_file, table_name,
                         columns, url)
    manager = DB_manager("Data/Database.db")
    print(manager.researchers_per_rating())
    app.run(debug=True)
