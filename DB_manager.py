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
        cursor.execute("SELECT Institution, count(Institution) FROM Researchers group by institution " +
                       "order by count(institution) DESC;")
        count_inst = cursor.fetchall()
        institutions = []
        frequencies = []
        for i in range(len(count_inst)):
            institutions.append(count_inst[i][0])
            frequencies.append(count_inst[i][1])
        return institutions , frequencies

    def researchers_per_rating(self):
        frequencies = [0, 0, 0, 0, 0]
        ratings = ["A", "B", "C", "P", "Y"]
        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()
        query = SQL_queries.count_records("Researchers", single_column="Rating")
        query += SQL_queries.group_by("Rating")
        cursor.execute(query)
        values = cursor.fetchall()
        for i in range(len(values)):
            frequencies[i] = (values[i][0])
        return ratings, frequencies

    def researcher_rating_by_inst(self, institution):
        frequencies = [0, 0, 0, 0, 0]
        ratings = ["A", "B", "C", "P", "Y"]
        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()
        query = SQL_queries.count_records("Researchers", single_column="Rating") + " WHERE "
        query += SQL_queries.compare_to_other("Institution", "\"" + institution + "\"", "=", )
        query += SQL_queries.group_by("Rating")
        cursor.execute(query)
        values = cursor.fetchall()
        for i in range(len(values)):
            frequencies[i] = (values[i][0])
        return ratings, frequencies
