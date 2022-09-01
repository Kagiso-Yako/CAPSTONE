# Kagiso Yako
# 31/08/2022
# Class for executing high level sqlite instructions and database interaction and management.

import sqlite3
from SQL_queries import SQL_queries

class DB_manager:
    def __init__(self, DB_name):
        self.__DB_name = DB_name
