# AI researchers are based at South Africa’s
# 26 public universities and other research-based organisations. They publish the results of their research in
# a variety of venues, including journals, conference proceedings and workshop proceedings. The
# application will draw from and consolidate data from multiple public research data sources, including the
# researcher rating system used by the National Research Foundation (NRF) and Microsoft Academic
# Graph (MAG). A web based interface must be provided for users to perform queries and visualise
# information about the research community including: a) dominant research areas/topics, publications
# venues, collaborations (co-authors) and impact (citations) (b) t++in which
# researchers are based (c) finding interesting trends and patterns over time, (c) appropriate metrics to
# assess and analyse the community and network structure, and (d) manual update and synchronisation
# functionality with MAG, the NRF and other public data sources.

import sqlite3
from flask import Flask, render_template, request
from Analysis import Analysis
from DB_auto_setup import DB_auto_setup
from SQL_queries import SQL_queries

# Global variables
# Defines the columns for the csv file and the columns for the NRF researchers table

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

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/researchers", methods=["GET"])
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
    finally:
        if rows is not None:
            return render_template("researchers.html", rows=rows, S_options=S_options, P_options=P_options,
                               Institutions=Institutions, Surnames=Surnames)
        else:
            return render_template("Error_page.html")


@app.route("/trendsAndAnalysis", methods=["GET", "POST"])
def trendsAndAnalysis():
    return render_template("TrendsAndAnalysis.html")

@app.route("/search_results")
def search_researchers():
    if request.method == "GET":
        rows = None
        try:
            item = request.args.get("researcher_search")
            operators = ["LIKE"] * len(columns_csv)
            wild_card_wrapped_item = "%" + item + "%"
            query = SQL_queries.get_subset(table_name, columns_csv, operators, to_one=wild_card_wrapped_item, wrap=True)
            conn = sqlite3.connect(NRF_database_file)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

        except sqlite3.Error:
            print("sqlite3.Error: Could not execute search.")
        finally:
            if rows is not None:
                if len(rows) > 0:
                    return render_template("search_researchers.html", rows=rows, length=len(rows))


@app.route("/institutions", methods=["GET", "POST"])
def institutions():
    rows = None
    try:
        conn = sqlite3.connect(NRF_database_file)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            cursor.execute(SQL_queries.get_table("Institutions"))
            rows = cursor.fetchall()
        except sqlite3.Error:
            print("Unable to obtain rows")
    except sqlite3.Error:
        print("Could not connect to database!")
    if rows is not None:
        res_vs_inst_JSON = my_JSONs.researchers_per_inst_JSON()
        return render_template("institutions.html", res_vs_I=res_vs_inst_JSON, rows=rows)
    else:
        return render_template("Error_page.html")


@app.route("/inst_<institution>")
def universityofcpt(institution):
    institution = institution.replace('+', ' ')
    institution_dist, values = my_JSONs.researcher_rating_by_inst_JSON(institution)
    my_sum = 0
    rows = None
    print(institution)
    try:
        conn = sqlite3.connect(NRF_database_file)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        quoted_inst = "\"" + institution + "\""
        cursor.execute(SQL_queries.get_table(table_name) + SQL_queries.compare_to_other("Institution",
                                                                                        quoted_inst, "=",
                                                                                        prefix="WHERE"))
        rows = cursor.fetchall()
        my_sum = sum(values)
    except sqlite3.Error:
        print("Failed to connect to database for the creation of institution.html")
    if rows is not None:
        return render_template("institution.html", institution_dist=institution_dist, institution=institution,
                           sum=my_sum, values=values, rows=rows)
    else:
        return render_template("Error_page.html")


if __name__ == '__main__':
    table = "Researchers"
    my_JSONs = Analysis()
    auto = DB_auto_setup(NRF_database_file, NRF_Excel_path, excel_sheet_name, columns_csv, csv_file, table_name,
                         columns, url)
    app.run(debug=True)
