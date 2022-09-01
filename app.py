from flask import Flask, render_template

from DB_auto_setup import DB_auto_setup
from DB_manager import DB_manager

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
    columns = ["id INTEGER primary key autoincrement",
               "Surname",
               "Initials",
               "Title",
               "Institution",
               "Rating",
               "Prim_Research",
               "Sec_Research",
               "Rating_Start",
               "Rating_Ending",
               "Specializations"]
    table = "Researchers"
    csv_columns = columns[1:len(columns)]  # The first column to be automatically generated
    my_DB_manager = DB_manager("Data/Database.db")
    auto = DB_auto_setup("Database2.db")
    auto.excel_to_csv("test/Current-Rated-Researchers-22-August-2022.xlsx", csv_columns)
    auto.csv_to_db("DB.csv", table, columns, "Database2.db")
    auto.download_from_url("https://www.nrf.ac.za/wp-content/uploads/2022/08/Current-Rated-Researchers-22-August"
                           + "-2022.xlsx")
    app.run(debug=True)
