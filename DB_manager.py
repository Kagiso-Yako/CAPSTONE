# Kagiso Yako
# 31/08/2022
# Class for executing high level sqlite instructions and database interaction and management.

import sqlite3
from SQL_queries import SQL_queries

class DB_manager:
    def __init__(self, DB_name):
        self.DB_name = DB_name

    def researchers_per_inst(self):
        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()
        cursor.execute("SELECT Institution, count(Institution) FROM Researchers group by institution;")
        count_inst = cursor.fetchall()
        institutions = []
        frequencies = []
        for i in range(len(count_inst)):
            institutions.append(count_inst[i][0])
            frequencies.append(count_inst[i][1])
        return institutions , frequencies

    def researchers_per_rating(self):
        ratings = ["A", "B", "C", "P", "Y"]
        frequencies = []
        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()

        for rating in ratings:
            query = SQL_queries.count_records("Researchers", single_column="Rating") + " WHERE "
            str_rating = "\""+rating+"\""
            query += SQL_queries.compare_to_other("Rating", str_rating, "=")
            cursor.execute(query)
            frequencies.append(cursor.fetchone()[0])

        return ratings, frequencies
