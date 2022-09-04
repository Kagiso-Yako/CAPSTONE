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


from flask import Flask, render_template

from DB_auto_setup import DB_auto_setup

# Global variables
# Defines the columns for the csv file and the columns for the NRF researchers table

table_name = "Researchers"
NRF_Excel_path = "Data/Current-Rated-Researchers-22-August-2022.xlsx"
excel_sheet_name = 'Current Rated Researchers (Webs'
csv_file = "DB.csv"
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
           "Prim_Research TEXT",
           "Sec_Research TEXT",
           "Specializations TEXT"]

columns_csv = ["Surname",
               "Initials",
               "Title",
               "Institution",
               "Rating",
               "Rating_Start",
               "Rating_Ending",
               "Prim_Research",
               "Sec_Research",
               "Specializations"]

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/researchers")
def researchers():
    return render_template("researchers.html")


@app.route("/institutions")
def institutions():
    return render_template("institutions.html")


@app.route("/delete")
def delete():
    return render_template("delete.html")


@app.route("/universityofcpt")
def universityofcpt():
    return render_template("institution.html")

if __name__ == '__main__':
    table = "Researchers"
    auto = DB_auto_setup(NRF_database_file, NRF_Excel_path, excel_sheet_name, columns_csv, csv_file, table_name,
                         columns, url)
    app.run(debug=True)
